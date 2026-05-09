from pydantic import BaseModel
from app.domain.bussiness_input import BusinessInput
from app.domain.idea_input import IdeaInput
from app.domain.market_input import MarketInput

class FeasabilityFormInput(BaseModel):
    idea: IdeaInput
    market: MarketInput
    business: BusinessInput