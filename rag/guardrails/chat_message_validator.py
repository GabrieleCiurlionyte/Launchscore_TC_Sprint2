import re


class ChatMessageValidationError(Exception):
    """Raised when a chatbot user message fails deterministic validation."""


MIN_MESSAGE_LENGTH = 3
MAX_MESSAGE_LENGTH = 800

SUSPICIOUS_PATTERNS = [
    r"ignore (all )?(previous|above) instructions",
    r"disregard (all )?(previous|above) instructions",
    r"reveal (the )?(system prompt|developer message|hidden instructions)",
    r"show (me )?(the )?(system prompt|developer message|hidden instructions)",
    r"print (the )?(system prompt|developer message|hidden instructions)",
    r"repeat (the )?(system prompt|developer message|hidden instructions)",
    r"bypass (your )?(rules|guardrails|safety)",
    r"act as (a|an) ",
    r"you are now ",
    r"jailbreak",
]

def ensure_valid_chat_message(message: str) -> str:
    cleaned_message = _normalize_message(message)

    if len(cleaned_message) < MIN_MESSAGE_LENGTH:
        raise ChatMessageValidationError(
            "Please enter a longer question so I can analyze it properly."
        )

    if len(cleaned_message) > MAX_MESSAGE_LENGTH:
        raise ChatMessageValidationError(
            f"Please keep the message under {MAX_MESSAGE_LENGTH} characters."
        )

    if not any(char.isalnum() for char in cleaned_message):
        raise ChatMessageValidationError(
            "Please enter a message with actual words or numbers."
        )

    if _contains_suspicious_pattern(cleaned_message):
        raise ChatMessageValidationError(
            "That message looks like an attempt to override internal instructions. "
            "Please ask a business or product question about your app idea instead."
        )

    return cleaned_message


def _normalize_message(message: str) -> str:
    collapsed_whitespace = re.sub(r"\s+", " ", message or "")
    return collapsed_whitespace.strip()


def _contains_suspicious_pattern(message: str) -> bool:
    normalized = message.casefold()
    return any(re.search(pattern, normalized) for pattern in SUSPICIOUS_PATTERNS)
