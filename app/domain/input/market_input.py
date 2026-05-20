from typing import Literal
from pydantic import BaseModel, Field

class MarketInput(BaseModel):
    pain_intensity: int = Field(ge=1, le=10)
    how_often_user_has_problem: Literal["Daily", "Weekly", "Monthly", "Rarely"]
    current_alternatives: list[str] = Field(default_factory=list)
    is_problem_paid_for_today: Literal["Yes", "No", "Not sure"]
