import sys
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from settings import get_settings
from rag.indexing.config import (
    PDF_PATHS,
    DEFAULT_CSV_PATH,
)
from rag.indexing.embedder import create_embeddings
from rag.indexing.index_documents import (
    index_pdf_documents,
    index_google_play_csv_documents,
)
from rag.indexing.vector_store import create_vector_store

def main() -> None:
    settings = get_settings()

    logger.info("Starting index build")

    embeddings = create_embeddings()

    pdf_vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=settings.persist_directory,
        collection_name=settings.pdf_collection_name,
    )
    logger.info("PDF vector store created.")

    csv_vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=settings.persist_directory,
        collection_name=settings.csv_collection_name,
    )
    logger.info("CSV vector store created.")

    pdf_vector_store.reset_collection()
    csv_vector_store.reset_collection()

    index_pdf_documents(
        vector_store=pdf_vector_store,
        pdf_paths=PDF_PATHS,
    )
    logger.info("PDF documents indexed.")

    index_google_play_csv_documents(
        vector_store=csv_vector_store,
        csv_path=DEFAULT_CSV_PATH,
    )
    logger.info("CSV documents indexed.")


if __name__ == "__main__":
    main()
