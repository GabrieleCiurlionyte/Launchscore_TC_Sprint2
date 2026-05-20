from typing import Literal
from pydantic import BaseModel, Field, model_validator

class BusinessInput(BaseModel):
    monetization_model: Literal[
        "Subscription",
        "Freemium",
        "Ads",
        "One-time purchase",
        "In-app purchases",
        "Marketplace fee",
        "Not sure",
    ]
    expected_price_eur: float = Field(ge=0)
    expected_price_period: Literal["Monthly", "Yearly", "One-time", "Free", "Not sure"]
    paid_features: list[str] = Field(default_factory=list)
    known_competitors: list[str] = Field(default_factory=list)
    differentiation: str
    build_budget_eur: int = Field(ge=0)
    timeline_months: int = Field(gt=0)
    team_size: int = Field(ge=1, le=50)

    @model_validator(mode="after")
    def validate_price_consistency(self):
        if self.expected_price_period == "Free" and self.expected_price_eur != 0:
            raise ValueError("Expected price must be 0 EUR when the price period is Free.")
        if self.expected_price_period != "Free" and self.expected_price_eur == 0:
            raise ValueError("Set a price above 0 EUR or choose Free as the price period.")
        if not self.differentiation.strip():
            raise ValueError("Question \"Why would users choose your app instead?\" is required.")
        return self
