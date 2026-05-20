import logging
import sqlite3

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_community.tools import BaseTool
from langgraph.checkpoint.sqlite import SqliteSaver

from rag.middleware.logging_middleware import log_rag_end, log_rag_start, monitor_tool
from rag.prompts.system_prompt import SYSTEM_PROMPT
from settings import get_settings
from rag.tools.make_retrieve_context_tool import make_retrieve_context_tool
from rag.tools.googleTrends.googleTrendsTool import google_trends
from rag.indexing.embedder import create_embeddings
from rag.indexing.vector_store import create_vector_store, get_document_count

logger = logging.getLogger(__name__)


def create_rag_agent():
    settings = get_settings()

    embeddings = create_embeddings()

    pdf_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=settings.persist_directory,
        collection_name=settings.pdf_collection_name,
    )

    csv_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=settings.persist_directory,
        collection_name=settings.csv_collection_name,
    )

    if get_document_count(pdf_store) == 0 or get_document_count(csv_store) == 0:
        raise RuntimeError(
            "The vector store is empty. Run `uv run python scripts/build_index.py` "
            "before starting the Streamlit app."
        )

    retrieve_pdf_context = create_retrieve_context_tool(
        pdf_store,
        "retrieve_pdf_context",
        "Use for market reports, trend narratives, strategic analysis from PDFs.",
    )

    retrieve_csv_context = create_retrieve_context_tool(
        csv_store,
        "retrieve_csv_context",
        "Use for app-level dataset facts (ratings, installs, category, pricing) from CSV.",
    )

    tools = [retrieve_pdf_context, retrieve_csv_context, google_trends]

    model = init_chat_model(
        settings.openai_model,
        api_key=settings.openai_api_key
    )
    
    checkpointer_connection = sqlite3.connect("checkpoints.db", check_same_thread=False)
    checkpointer = SqliteSaver(checkpointer_connection)

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
        middleware=[log_rag_start, monitor_tool, log_rag_end]
    )

def create_retrieve_context_tool(vector_store : Chroma, context_name: str, tool_description: str) -> BaseTool:
    retrieve_context = make_retrieve_context_tool(vector_store)
    retrieve_context.name = context_name
    retrieve_context.description = tool_description
    return retrieve_context
