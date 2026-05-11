import logging
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.loaders.pdf_loader import PdfLoader

logger = logging.getLogger(__name__)


def index_pdf_documents(vector_store, pdf_path: Path):
    loader = PdfLoader()
    docs = loader.load_pdf_data(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    split_docs = splitter.split_documents(docs)

    document_ids = vector_store.add_documents(split_docs)
    logger.info("Indexed %s document chunks", len(document_ids))
    return document_ids
