from typing import List
from pydantic import BaseModel

class SWOTOutput(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    overall_assessment: str