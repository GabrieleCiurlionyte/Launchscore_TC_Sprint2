# rag/llm/model_factory.py

from functools import lru_cache
from typing import Any, Type

from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter
from pydantic import BaseModel

from settings import get_settings


DEFAULT_MODEL_KWARGS = {
    "temperature": 0,
    "timeout": 20,
    "max_tokens": 1000,
    "max_retries": 2,
}

@lru_cache(maxsize=1)
def get_rate_limiter() -> InMemoryRateLimiter:
    return InMemoryRateLimiter(
        requests_per_second=0.5,
        check_every_n_seconds=0.1,
        max_bucket_size=5,
    )

def create_chat_model(
    *,
    use_rate_limiter: bool = True,
    **kwargs: Any,
):
    settings = get_settings()

    model_kwargs = {
        **DEFAULT_MODEL_KWARGS,
        **kwargs,
    }

    if use_rate_limiter:
        model_kwargs["rate_limiter"] = get_rate_limiter()

    return init_chat_model(
        settings.openai_model,
        api_key=settings.openai_api_key,
        **model_kwargs,
    )

def create_structured_chat_model(
    output_schema: Type[BaseModel],
    *,
    use_rate_limiter: bool = True,
    **kwargs: Any,
):
    return create_chat_model(
        use_rate_limiter=use_rate_limiter,
        **kwargs,
    ).with_structured_output(output_schema)