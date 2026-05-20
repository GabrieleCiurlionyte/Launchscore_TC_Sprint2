import logging

from langchain_chroma import Chroma

logger = logging.getLogger(__name__)

def create_vector_store(embeddings, persist_directory: str, collection_name: str):
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    logger.info("Vector store loaded for collection '%s'", collection_name)
    return vector_store


def get_document_count(vector_store: Chroma) -> int:
    return vector_store._collection.count()