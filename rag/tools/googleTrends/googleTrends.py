from __future__ import annotations

import logging
import time
from dataclasses import dataclass, asdict
from typing import Any

from pytrends import exceptions as pytrends_exceptions
from pytrends.request import TrendReq

logger = logging.getLogger(__name__)


@dataclass
class TrendsResult:
    keyword: str
    geo: str
    timeframe: str
    trend_direction: str
    growth_90d_pct: float | None
    latest_score: float | None
    avg_score: float | None
    peak_score: float | None
    top_regions: list[dict[str, Any]]


class GoogleTrendsClient:
    def __init__(self, hl: str = "en-US", tz: int = 180) -> None:
        self.client = TrendReq(hl=hl, tz=tz)

    def run(
        self,
        keyword: str,
        geo: str = "",
    ) -> TrendsResult:
        timeframe = "today 12-m"
        category = 0

        log = logging.LoggerAdapter(
            logger,
            {
                "keyword": keyword,
                "geo": geo or "GLOBAL",
                "timeframe": timeframe,
            },
        )

        log.info("Building Google Trends payload")
        self.client.build_payload(
            kw_list=[keyword],
            cat=category,
            timeframe=timeframe,
            geo=geo,
        )

        iot = None

        for attempt in range(3):
            try:
                iot = self.client.interest_over_time()
                break
            except pytrends_exceptions.TooManyRequestsError:
                wait_seconds = 2 ** (attempt + 1)
                log.warning(
                    "Google Trends rate limited request, retrying in %s seconds",
                    wait_seconds,
                )
                time.sleep(wait_seconds)

        if iot is None:
            log.warning("Google Trends remained unavailable after retries")
            return TrendsResult(
                keyword=keyword,
                geo=geo,
                timeframe=timeframe,
                trend_direction="unknown",
                growth_90d_pct=None,
                latest_score=None,
                avg_score=None,
                peak_score=None,
                top_regions=[],
            )

        if iot.empty:
            log.warning("No Google Trends data returned")
            raise ValueError(f"No Google Trends data returned for keyword={keyword!r}")

        series = iot[keyword].astype(float)

        latest_score = float(series.iloc[-1])
        avg_score = float(series.mean())
        peak_score = float(series.max())

        log.info(
            "Fetched %s points latest=%.2f avg=%.2f peak=%.2f",
            len(series),
            latest_score,
            avg_score,
            peak_score,
        )

        growth_90d_pct = None
        if len(series) >= 90:
            past = float(series.iloc[-90])
            now = float(series.iloc[-1])
            if past > 0:
                growth_90d_pct = ((now - past) / past) * 100.0

        trend_direction = "flat"
        if growth_90d_pct is not None:
            if growth_90d_pct > 15:
                trend_direction = "rising"
            elif growth_90d_pct < -15:
                trend_direction = "falling"

        try:
            regions_df = self.client.interest_by_region(
                resolution="COUNTRY",
                inc_low_vol=False,
            )
            top_regions = (
                regions_df.sort_values(by=keyword, ascending=False)
                .head(10)[[keyword]]
                .reset_index()
                .rename(columns={keyword: "score"})
                .to_dict(orient="records")
            )
        except Exception:
            log.warning("Interest by region data is unavailable")
            top_regions = []

        return TrendsResult(
            keyword=keyword,
            geo=geo,
            timeframe=timeframe,
            trend_direction=trend_direction,
            growth_90d_pct=growth_90d_pct,
            latest_score=latest_score,
            avg_score=avg_score,
            peak_score=peak_score,
            top_regions=top_regions,
        )


if __name__ == "__main__":
    tool = GoogleTrendsClient()
    result = tool.run("habit tracker", geo="US")
    print(asdict(result))