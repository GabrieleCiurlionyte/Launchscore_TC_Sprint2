import sys
from pathlib import Path

from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.indexing.config import DEFAULT_PDF_PATH, PERSIST_DIRECTORY
from rag.indexing.embedder import create_embeddings
from rag.indexing.index_documents import index_pdf_documents
from rag.indexing.vector_store import create_vector_store


def main() -> None:
    load_dotenv()

    logger.info("Starting index build")
    
    embeddings = create_embeddings()
    
    vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )
    
    logger.info("Vector store created.")

    vector_store.reset_collection()

    pdf_path = Path(DEFAULT_PDF_PATH)
    index_pdf_documents(vector_store=vector_store, pdf_path=pdf_path)
    logger.info("Documents indexed.")


if __name__ == "__main__":
    main()
