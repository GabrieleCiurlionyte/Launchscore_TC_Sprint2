from pydantic import BaseModel, Field, model_validator
from app.domain.monetization_model import MonetizationModel
from app.domain.payment_period import PaymentPeriod

class BusinessInput(BaseModel):
    monetization_model: MonetizationModel
    expected_price_eur: float = Field(ge=0)
    expected_price_period: PaymentPeriod
    paid_features: list[str] = Field(default_factory=list)
    known_competitors: list[str] = Field(default_factory=list)
    differentiation: str
    build_budget_eur: int = Field(ge=0)
    timeline_months: int = Field(gt=0)
    team_size: int = Field(ge=1, le=50)

    @model_validator(mode="after")
    def validate_price_consistency(self):
        if self.expected_price_period == PaymentPeriod.FREE and self.expected_price_eur != 0:
            raise ValueError("Expected price must be 0 EUR when the price period is Free.")
        if self.expected_price_period != PaymentPeriod.FREE and self.expected_price_eur == 0:
            raise ValueError("Set a price above 0 EUR or choose Free as the price period.")
        if not self.differentiation.strip():
            raise ValueError("Question \"Why would users choose your app instead?\" is required.")
        return self
