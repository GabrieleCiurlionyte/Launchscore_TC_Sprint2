import logging
from typing import Optional

from langchain.tools import tool

from app.domain.input.bussiness_input import BusinessInput
from app.domain.input.feasability_form_input import FeasabilityFormInput
from app.domain.input.idea_input import IdeaInput
from app.domain.input.market_input import MarketInput
from app.domain.monetization_model import MonetizationModel
from app.domain.payment_period import PaymentPeriod
from rag.tools.revenueProjection.models.revenue_projection_output import RevenueProjectionOutput
from rag.tools.revenueProjection.models.revenue_scenario import RevenueScenario
from rag.tools.revenueProjection.revenue_projection_helpers import estimate_monthly_operational_costs, normalize_monthly_price
from rag.tools.revenueProjection.revenue_scenario_defaults import RevenueScenarioDefaults, get_revenue_projection_defaults


logger = logging.getLogger(__name__)

STORE_FEE_RATE = 0.15

@tool(args_schema=FeasabilityFormInput)
def estimate_revenue_projection(
    idea: IdeaInput,
    market: MarketInput,
    business: BusinessInput,
) -> dict:
    """
    Estimate simple app revenue projection using the app idea, market, and business model.

    Produces conservative, base, and optimistic monthly revenue scenarios.
    """

    logger.info(
        "Calling revenue projection tool | idea=%s | monetization=%s | price=%s %s",
        idea.one_sentence_pitch,
        business.monetization_model,
        business.expected_price_eur,
        business.expected_price_period,
    )

    try:
        monthly_price = normalize_monthly_price(
            price=business.expected_price_eur,
            period=business.expected_price_period,
        )

        assumptions = get_revenue_projection_defaults(
            monetization_model=business.monetization_model
        )

        warnings = _build_projection_warnings(
            business=business,
            monthly_price=monthly_price,
        )

        scenarios: list[RevenueScenario] = [
            _calculate_scenario_revenue(
                scenario=scenario,
                business=business,
                monthly_price=monthly_price,
            )
            for scenario in assumptions
        ]

        output = RevenueProjectionOutput(
            monetization_model=business.monetization_model,
            expected_price_eur=business.expected_price_eur,
            expected_price_period=business.expected_price_period,
            scenarios=scenarios,
            summary=(
                "This is a rough scenario-based revenue projection using default "
                "early-stage app assumptions. It should be treated as an estimate, "
                "not a validated financial forecast."
            ),
            warnings=warnings,
        )

        logger.info(
            "Revenue projection generated successfully | scenarios=%d",
            len(output.scenarios),
        )

        return output.model_dump()

    except Exception as e:
        logger.exception("Revenue projection generation failed")
        raise RuntimeError(f"Failed to generate revenue projection: {e}") from e
    
def _build_projection_warnings(
    business: BusinessInput,
    monthly_price: float,
) -> list[str]:
    warnings: list[str] = []

    if business.monetization_model == MonetizationModel.NOT_SURE:
        warnings.append(
            "The monetization model is not defined, so this projection uses generic assumptions."
        )

    if business.expected_price_period == PaymentPeriod.NOT_SURE:
        warnings.append(
            "The price period is not defined, so the monthly price may be unreliable."
        )

    if monthly_price == 0 and business.monetization_model != MonetizationModel.ADS:
        warnings.append(
            "Expected monthly price is 0 EUR. Revenue may be underestimated unless the app uses ads or another indirect model."
        )

    return warnings

def _calculate_scenario_revenue(
    scenario: RevenueScenarioDefaults,
    business: BusinessInput,
    monthly_price: float,
) -> RevenueScenario:
    paying_users = int(
        scenario.estimated_monthly_users * scenario.paid_conversion_rate
    )

    if business.monetization_model == MonetizationModel.ADS:
        gross_revenue = (
            scenario.estimated_monthly_users
            * (scenario.monthly_ad_revenue_per_user or 0.0)
        )
    else:
        gross_revenue = paying_users * monthly_price

    store_fee = gross_revenue * STORE_FEE_RATE
    net_revenue = gross_revenue - store_fee

    monthly_costs = estimate_monthly_operational_costs(
        build_budget_eur=business.build_budget_eur,
        timeline_months=business.timeline_months,
        team_size=business.team_size,
        monthly_cost_multiplier=scenario.monthly_cost_multiplier,
    )

    monthly_profit = net_revenue - monthly_costs

    if monthly_profit > 0:
        break_even_months: Optional[float] = (
            business.build_budget_eur / monthly_profit
        )
    else:
        break_even_months = None

    return RevenueScenario(
        scenario_name=scenario.scenario_name,
        estimated_monthly_users=scenario.estimated_monthly_users,
        paid_conversion_rate=round(scenario.paid_conversion_rate, 4),
        paying_users=paying_users,
        gross_monthly_revenue_eur=round(gross_revenue, 2),
        store_fee_eur=round(store_fee, 2),
        net_monthly_revenue_eur=round(net_revenue, 2),
        estimated_monthly_costs_eur=round(monthly_costs, 2),
        estimated_monthly_profit_eur=round(monthly_profit, 2),
        break_even_months=round(break_even_months, 1)
        if break_even_months is not None
        else None,
    )
