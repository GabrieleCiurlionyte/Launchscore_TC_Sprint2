import sys
from pathlib import Path
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.indexing.config import (
    DEFAULT_PDF_PATH,
    DEFAULT_CSV_PATH,
    PERSIST_DIRECTORY,
    PDF_COLLECTION_NAME,
    CSV_COLLECTION_NAME,
)
from rag.indexing.embedder import create_embeddings
from rag.indexing.index_documents import (
    index_pdf_documents,
    index_google_play_csv_documents,
)
from rag.indexing.vector_store import create_vector_store

def main() -> None:
    load_dotenv()

    logger.info("Starting index build")

    embeddings = create_embeddings()

    pdf_vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=PDF_COLLECTION_NAME,
    )
    logger.info("PDF vector store created.")

    csv_vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=CSV_COLLECTION_NAME,
    )
    logger.info("CSV vector store created.")

    pdf_vector_store.reset_collection()
    csv_vector_store.reset_collection()

    pdf_path = Path(DEFAULT_PDF_PATH)
    index_pdf_documents(
        vector_store=pdf_vector_store,
        pdf_path=pdf_path,
    )
    logger.info("PDF documents indexed.")

    csv_path = Path(DEFAULT_CSV_PATH)
    index_google_play_csv_documents(
        vector_store=csv_vector_store,
        csv_path=csv_path,
    )
    logger.info("CSV documents indexed.")


if __name__ == "__main__":
    main()