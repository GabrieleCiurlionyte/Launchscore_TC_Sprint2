from langchain_community.document_loaders.csv_loader import CSVLoader
from pathlib import Path

class CsvLoader:
    def load_csv_data(self, file_path: str | Path):
        loader = CSVLoader(
            file_path=str(file_path),
            encoding="utf-8-sig",
            csv_args={
                "delimiter": ",",
                "quotechar": '"',
            })
        return loader.load()