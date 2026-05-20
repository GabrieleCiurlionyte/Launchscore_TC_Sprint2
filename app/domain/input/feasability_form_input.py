from pydantic import BaseModel
from app.domain.input.bussiness_input import BusinessInput
from app.domain.input.idea_input import IdeaInput
from app.domain.input.market_input import MarketInput

class FeasabilityFormInput(BaseModel):
    idea: IdeaInput
    market: MarketInput
    business: BusinessInput