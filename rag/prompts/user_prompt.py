from app.domain.feasability_form_input import FeasabilityFormInput


def build_feasibility_user_prompt(form_input: FeasabilityFormInput) -> str:
    return f"""
Analyze the following mobile app idea for business feasibility.

Use the provided form data as the primary source of truth.
Use retrieval tools when needed to validate market demand, competition, and trends.
Do not invent facts when evidence is missing.

Form input:
{form_input.model_dump_json(indent=2)}

Focus your analysis on:
- profitability potential
- market risks
- competitors
- MVP scope
- monetization strategy
- whether this idea should move forward
""".strip()
