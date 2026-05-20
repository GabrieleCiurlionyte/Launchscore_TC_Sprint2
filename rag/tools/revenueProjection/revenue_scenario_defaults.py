from enum import Enum

from app.domain.monetization_model import MonetizationModel
from pydantic import BaseModel

class RevenueScenariosName(str, Enum):
    CONSERVATIVE = "Conservative"
    BASE = "Base"
    OPTIMISTIC = "Optimistic"

class RevenueScenarioDefaults(BaseModel):
    scenario_name: RevenueScenariosName
    estimated_monthly_users: int
    paid_conversion_rate: float
    monthly_cost_multiplier: float
    monthly_ad_revenue_per_user: float | None = None

def get_revenue_projection_defaults(
    monetization_model: MonetizationModel,
) -> list[RevenueScenarioDefaults]:
    """
    Returns simple default assumptions for early-stage app revenue projection.

    Later they will be replaced by competitor benchmarks, user-provided assumptions, RAG-retrieved market data
    """

    if monetization_model == MonetizationModel.SUBSCRIPTION:
        return [
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.CONSERVATIVE,
                estimated_monthly_users=500,
                paid_conversion_rate=0.01,
                monthly_cost_multiplier=0.05,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.BASE,
                estimated_monthly_users=2_000,
                paid_conversion_rate=0.03,
                monthly_cost_multiplier=0.08,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.OPTIMISTIC,
                estimated_monthly_users=8_000,
                paid_conversion_rate=0.06,
                monthly_cost_multiplier=0.12,
            ),
        ]

    if monetization_model == MonetizationModel.FREEMIUM:
        return [
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.CONSERVATIVE,
                estimated_monthly_users=1_000,
                paid_conversion_rate=0.005,
                monthly_cost_multiplier=0.05,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.BASE,
                estimated_monthly_users=5_000,
                paid_conversion_rate=0.02,
                monthly_cost_multiplier=0.08,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.OPTIMISTIC,
                estimated_monthly_users=20_000,
                paid_conversion_rate=0.05,
                monthly_cost_multiplier=0.12,
            ),
        ]

    if monetization_model == MonetizationModel.ONE_TIME_PURCHASE:
        return [
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.CONSERVATIVE,
                estimated_monthly_users=300,
                paid_conversion_rate=0.01,
                monthly_cost_multiplier=0.04,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.BASE,
                estimated_monthly_users=1_500,
                paid_conversion_rate=0.025,
                monthly_cost_multiplier=0.06,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.OPTIMISTIC,
                estimated_monthly_users=6_000,
                paid_conversion_rate=0.05,
                monthly_cost_multiplier=0.10,
            ),
        ]

    if monetization_model == MonetizationModel.IN_APP_PURCHASES:
        return [
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.CONSERVATIVE,
                estimated_monthly_users=1_000,
                paid_conversion_rate=0.005,
                monthly_cost_multiplier=0.05,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.BASE,
                estimated_monthly_users=5_000,
                paid_conversion_rate=0.02,
                monthly_cost_multiplier=0.08,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.OPTIMISTIC,
                estimated_monthly_users=25_000,
                paid_conversion_rate=0.04,
                monthly_cost_multiplier=0.12,
            ),
        ]

    if monetization_model == MonetizationModel.ADS:
        return [
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.CONSERVATIVE,
                estimated_monthly_users=2_000,
                paid_conversion_rate=0.0,
                monthly_ad_revenue_per_user=0.03,
                monthly_cost_multiplier=0.05,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.BASE,
                estimated_monthly_users=10_000,
                paid_conversion_rate=0.0,
                monthly_ad_revenue_per_user=0.08,
                monthly_cost_multiplier=0.08,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.OPTIMISTIC,
                estimated_monthly_users=50_000,
                paid_conversion_rate=0.0,
                monthly_ad_revenue_per_user=0.15,
                monthly_cost_multiplier=0.12,
            ),
        ]

    if monetization_model == MonetizationModel.MARKETPLACE_FEE:
        return [
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.CONSERVATIVE,
                estimated_monthly_users=500,
                paid_conversion_rate=0.02,
                monthly_cost_multiplier=0.06,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.BASE,
                estimated_monthly_users=2_500,
                paid_conversion_rate=0.05,
                monthly_cost_multiplier=0.10,
            ),
            RevenueScenarioDefaults(
                scenario_name=RevenueScenariosName.OPTIMISTIC,
                estimated_monthly_users=10_000,
                paid_conversion_rate=0.08,
                monthly_cost_multiplier=0.15,
            ),
        ]

    return [
        RevenueScenarioDefaults(
            scenario_name=RevenueScenariosName.CONSERVATIVE,
            estimated_monthly_users=500,
            paid_conversion_rate=0.005,
            monthly_cost_multiplier=0.05,
        ),
        RevenueScenarioDefaults(
            scenario_name=RevenueScenariosName.BASE,
            estimated_monthly_users=2_000,
            paid_conversion_rate=0.02,
            monthly_cost_multiplier=0.08,
        ),
        RevenueScenarioDefaults(
            scenario_name=RevenueScenariosName.OPTIMISTIC,
            estimated_monthly_users=8_000,
            paid_conversion_rate=0.05,
            monthly_cost_multiplier=0.12,
        ),
    ]
