import logging
from pathlib import Path
from typing import Iterable

from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.loaders.pdf_loader import PdfLoader
from rag.loaders.csv_loader import CSVLoader
from rag.utils.google_play_document_formatter import prepare_google_play_document

logger = logging.getLogger(__name__)

pdf_loader = PdfLoader()

pdf_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

csv_loader = CSVLoader()

def index_pdf_documents(vector_store, pdf_paths: Iterable[Path]):
    
    all_split_docs = []

    for pdf_path in pdf_paths:
        docs = pdf_loader.load_pdf_data(pdf_path)

        split_docs = pdf_splitter.split_documents(docs)
        all_split_docs.extend(split_docs)

        logger.info(
            "Prepared %s chunks from %s",
            len(split_docs),
            pdf_path.name,
        )

    document_ids = vector_store.add_documents(all_split_docs)

    logger.info(
        "Indexed %s total PDF chunks",
        len(document_ids),
    )

    return document_ids

def index_google_play_csv_documents(vector_store, csv_path: Path):

    docs = csv_loader.load_csv_data(csv_path)

    cleaned_docs = []
    for doc in docs:
        cleaned_doc = prepare_google_play_document(doc)
        cleaned_docs.append(cleaned_doc)
        
    logger.info("Finished preparing %s Goggle Play store documents", len(cleaned_docs))

    document_ids = vector_store.add_documents(cleaned_docs)
    logger.info("Indexed %s CSV rows", len(document_ids))
    return document_ids