import logging
from pathlib import Path

from rag.loaders.pdf_loader import PdfLoader
from rag.splitters.document_splitter import DocumentSplitter

logger = logging.getLogger(__name__)


def index_pdf_documents(vector_store, pdf_path: Path):
    loader = PdfLoader()
    docs = loader.load_pdf_data(pdf_path)

    splitter = DocumentSplitter()
    split_docs = splitter.RecursivellySplitDocument(docs=docs)

    document_ids = vector_store.add_documents(split_docs)
    logger.info("Indexed %s document chunks", len(document_ids))
    return document_ids
