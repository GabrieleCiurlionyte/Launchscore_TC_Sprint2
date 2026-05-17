from pathlib import Path

PERSIST_DIRECTORY = "./chroma_langchain.db"

PDF_COLLECTION_NAME = "pdf_market_reports"
CSV_COLLECTION_NAME = "google_play_apps"

DEFAULT_PDF_PATH = Path("data/raw_pdfs/sensor_tower__state_of_mobile_2026__en.pdf")
DEFAULT_CSV_PATH = Path("data/csv/googleplaystore.csv")