def format_bussiness_context(form_data: dict) -> str:
    idea = form_data.get("idea", {})
    market = form_data.get("market", {})
    business = form_data.get("business", {})

    price_period = business.get("expected_price_period", "")
    if hasattr(price_period, "value"):
        price_period = price_period.value

    return f"""
Idea:
- Pitch: {idea.get("one_sentence_pitch", "")}
- Problem: {idea.get("problem_solved", "")}
- Target users: {idea.get("target_users", "")}
- Target countries: {", ".join(idea.get("target_countries", [])) or "Not specified"}

Market:
- Pain intensity: {market.get("pain_intensity", "")}/10
- Frequency: {market.get("how_often_user_has_problem", "")}
- Alternatives: {", ".join(market.get("current_alternatives", [])) or "Not specified"}
- Users already pay: {market.get("is_problem_paid_for_today", "")}

Business:
- Monetization: {business.get("monetization_model", "")}
- Price: {business.get("expected_price_eur", "")} EUR ({price_period})
- Paid features: {", ".join(business.get("paid_features", [])) or "Not specified"}
- Competitors: {", ".join(business.get("known_competitors", [])) or "Not specified"}
- Differentiation: {business.get("differentiation", "")}
- Budget: {business.get("build_budget_eur", "")} EUR
- Timeline: {business.get("timeline_months", "")} months
- Team size: {business.get("team_size", "")}
""".strip()