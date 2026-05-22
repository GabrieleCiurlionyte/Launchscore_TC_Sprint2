from typing import Optional
from pydantic import BaseModel

from rag.tools.revenueProjection.revenue_scenario_defaults import RevenueScenariosName

class RevenueScenario(BaseModel):
    scenario_name: RevenueScenariosName

    estimated_monthly_users: int
    paid_conversion_rate: float
    paying_users: int

    gross_monthly_revenue_eur: float
    store_fee_eur: float
    net_monthly_revenue_eur: float

    estimated_monthly_costs_eur: float
    estimated_monthly_profit_eur: float

    break_even_months: Optional[float]
