import logging

from langchain_chroma import Chroma

logger = logging.getLogger(__name__)

def create_vector_store(embeddings, persist_directory: str):
    vector_store = Chroma(
        collection_name="rag_collection",
        embedding_function=embeddings,
        persist_directory=persist_directory,
    )
    logger.info("Vector store loaded")
    return vector_store


def get_document_count(vector_store: Chroma) -> int:
    return vector_store._collection.count()
