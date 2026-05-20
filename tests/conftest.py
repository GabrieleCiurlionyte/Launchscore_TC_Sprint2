import os

from settings import get_settings

settings = get_settings()

# Keep tests that inspect os.environ working while using pydantic settings
os.environ.setdefault("OPENAI_API_KEY", settings.openai_api_key)
