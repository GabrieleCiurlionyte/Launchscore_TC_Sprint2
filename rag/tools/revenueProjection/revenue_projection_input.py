from pydantic import BaseModel, Field


class RevenueProjectionInput(BaseModel):
    monthly_active_users: int = Field(..., gt=0)

    subscription_conversion_rate: float = Field(
        ..., ge=0, le=1,
        description="Percent of users converting to paid subscriptions"
    )

    subscription_price: float = Field(..., gt=0)

    ad_revenue_per_user: float = Field(
        0.0,
        ge=0,
        description="Average monthly ad revenue per free user"
    )

    monthly_infrastructure_cost: float = Field(..., ge=0)

    monthly_marketing_cost: float = Field(..., ge=0)

    initial_development_cost: float = Field(..., ge=0)

    store_fee_rate: float = Field(
        0.30,
        ge=0,
        le=1,
        description="Apple/Google store fee"
    )

    churn_rate: float = Field(
        0.05,
        ge=0,
        le=1,
        description="Monthly subscriber churn"
    )