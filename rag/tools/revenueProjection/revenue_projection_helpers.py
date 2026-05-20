from app.domain.payment_period import PaymentPeriod

def normalize_monthly_price(price: float, period: PaymentPeriod) -> float:
    if period == PaymentPeriod.MONTHLY:
        return price

    if period == PaymentPeriod.YEARLY:
        return price / 12

    if period == PaymentPeriod.ONE_TIME:
        # For a simple first version, spread one-time purchase over 12 months.
        return price / 12

    if period in {PaymentPeriod.FREE, PaymentPeriod.NOT_SURE}:
        return 0.0

    return 0.0

def estimate_monthly_operational_costs(
    build_budget_eur: int,
    timeline_months: int,
    team_size: int,
    monthly_cost_multiplier: float,
) -> float:
    """
    Very rough operating cost estimate.

    build_budget_eur / timeline_months approximates development burn.
    multiplier adds hosting/API/tools/support overhead.
    """

    development_burn = build_budget_eur / max(timeline_months, 1)
    overhead = build_budget_eur * monthly_cost_multiplier / 12

    team_overhead = team_size * 50

    return development_burn + overhead + team_overhead