from pydantic import BaseModel


class SWOTOutput(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]