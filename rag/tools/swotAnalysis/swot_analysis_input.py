from pydantic import BaseModel, Field

class SWOTInput(BaseModel):
    idea_summary: str = Field(..., description="Short description of the idea", min_length=10, max_length=2000)
    target_market: str = Field(..., description="Primary target market", max_length=1000)
    context: str = Field("", description="Optional market/retrieval context", max_length=6000)