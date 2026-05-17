import logging
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.loaders.pdf_loader import PdfLoader
from rag.loaders.csv_loader import CSVLoader
from rag.utils.google_play_document_formatter import prepare_google_play_document

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

def index_google_play_csv_documents(vector_store, csv_path: Path):
    loader = CSVLoader()
    docs = loader.load_csv_data(csv_path)

    cleaned_docs = []
    for doc in docs:
        cleaned_doc = prepare_google_play_document(doc)
        cleaned_docs.append(cleaned_doc)
    logger.info("Finished preparing %s Goggle Play store documents", len(cleaned_docs))

    document_ids = vector_store.add_documents(cleaned_docs)
    logger.info("Indexed %s CSV rows", len(document_ids))
    return document_ids