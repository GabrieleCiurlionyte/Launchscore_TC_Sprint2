def normalize_monthly_price(price: float, period: str) -> float:
    """
    Converts the user's expected price into a monthly price.
    """
    if period == "Monthly":
        return price

    if period == "Yearly":
        return price / 12

    if period == "One-time":
        return price / 12

    if period in ["Free", "Not sure"]:
        return 0.0

    return 0.0