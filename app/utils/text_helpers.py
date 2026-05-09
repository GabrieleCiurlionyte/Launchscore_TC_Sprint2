def split_comma_text(value: str):
    return [item.strip() for item in value.split(",") if item.strip()]