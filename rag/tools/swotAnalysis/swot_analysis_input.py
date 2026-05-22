import re

from pydantic import BaseModel, Field, field_validator

class SWOTInput(BaseModel):
    idea_summary: str = Field(..., description="Short description of the idea", min_length=10, max_length=2000)
    target_market: str = Field(..., description="Primary target market", max_length=1000)
    context: str = Field("", description="Optional market/retrieval context", max_length=6000)

    @field_validator("idea_summary", "target_market", "context", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        if value is None:
            return ""

        normalized = str(value).replace("\x00", "")
        normalized = re.sub(r"\s+", " ", normalized)
        return normalized.strip()
