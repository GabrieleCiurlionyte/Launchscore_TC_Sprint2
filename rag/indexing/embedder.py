from langchain_openai import OpenAIEmbeddings
from settings import get_settings

def create_embeddings():
    settings = get_settings()
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
