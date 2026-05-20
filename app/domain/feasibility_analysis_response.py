# app/domain/feasibility_analysis_response.py
from typing import Literal
from pydantic import BaseModel, Field


class FeasibilityAnalysisResponse(BaseModel):
    profitability_score: int = Field(description="Profitability score from 0 to 100.")
    market_risk_analysis: str = Field(description="Short analysis of the main market risks.")
    competitor_summary: str = Field(description="Brief summary of the competitive landscape.")
    mvp_recommendation: str = Field(description="Recommended MVP scope or direction.")
    monetization_recommendation: str = Field(description="Best-fit monetization approach.")
    go_or_no_go_decision: Literal["go", "no-go", "needs-validation"] = Field(
        description="Final recommendation on whether to proceed."
    )
