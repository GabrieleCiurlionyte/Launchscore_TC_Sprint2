from pydantic import BaseModel, Field

from rag.tools.revenueProjection.models.revenue_scenario import RevenueScenario

class RevenueProjectionOutput(BaseModel):
    monetization_model: str
    expected_price_eur: float
    expected_price_period: str

    scenarios: list[RevenueScenario]

    summary: str
    warnings: list[str] = Field(default_factory=list)