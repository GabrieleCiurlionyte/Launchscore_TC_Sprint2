from pydantic import BaseModel, Field

class SWOTInput(BaseModel):
    idea_summary: str = Field(..., description="Short description of the idea")
    target_market: str = Field(..., description="Primary target market")
    context: str = Field("", description="Optional market/retrieval context")