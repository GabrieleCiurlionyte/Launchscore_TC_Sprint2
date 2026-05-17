from pathlib import Path

PERSIST_DIRECTORY = "./chroma_langchain.db"

PDF_COLLECTION_NAME = "pdf_market_reports"
CSV_COLLECTION_NAME = "google_play_apps"

PDF_PATHS = [
    Path("data/raw_pdfs/sensor_tower__state_of_mobile_2026__en.pdf"),
    Path("data/raw_pdfs/sensor_tower__state_of_web_2026.pdf"),
    Path("data/raw_pdfs/sensor_tower__predictions_for_the_digital_economy_in_2026.pdf"),
    Path("data/raw_pdfs/sensor_tower__order_up_qsr_spotlight_report_2026.pdf"),
]

DEFAULT_CSV_PATH = Path("data/csv/googleplaystore.csv")