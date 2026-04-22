from langchain_community.document_loaders import PyPDFLoader

from langchain_community.document_loaders import PyPDFLoader


class PdfLoader:
    def load_pdf_data(self, file_path: str):
        loader = PyPDFLoader(file_path)

        pages = []
        for doc in loader.lazy_load():
            pages.append(doc)

        return pages
