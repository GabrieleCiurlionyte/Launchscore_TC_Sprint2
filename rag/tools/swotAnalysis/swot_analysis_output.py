from pydantic import BaseModel, Field


class SWOTOutput(BaseModel):
    strengths: list[str] = Field(..., min_length=1)
    weaknesses: list[str] = Field(..., min_length=1)
    opportunities: list[str] = Field(..., min_length=1)
    threats: list[str] = Field(..., min_length=1)
    overall_assessment: str = Field(..., min_length=20, max_length=1500)
