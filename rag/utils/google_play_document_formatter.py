from langchain_core.documents import Document

def prepare_google_play_document(doc: Document) -> Document:

    fields = {}

    for line in doc.page_content.split("\n"):

        if ": " in line:
            key, value = line.split(": ", 1)
            fields[key.strip()] = value.strip()

    app = fields.get("App", "")
    category = fields.get("Category", "")
    rating = fields.get("Rating", "")
    installs = fields.get("Installs", "")
    genres = fields.get("Genres", "")
    content_rating = fields.get("Content Rating", "")

    content = f"""
    {app} is an Android app in the {category} category.

    It belongs to the genres: {genres}.

    The app has a rating of {rating}
    and approximately {installs} installs.

    The target audience is {content_rating}.
    """.strip()

    metadata = {
        **doc.metadata,
        "source_type": "google_play_csv",
        "app_name": app,
        "category": category,
        "rating": rating,
        "installs": installs,
    }

    return Document(
        page_content=content,
        metadata=metadata,
    )