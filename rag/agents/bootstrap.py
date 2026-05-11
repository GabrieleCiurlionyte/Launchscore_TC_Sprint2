import logging
import sqlite3

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite import SqliteSaver

from app.domain.feasibility_analysis_response import FeasibilityAnalysisResponse
from rag.indexing.config import PERSIST_DIRECTORY
from rag.tools.make_retrieve_context_tool import make_retrieve_context_tool
from rag.tools.googleTrends.googleTrendsTool import google_trends
from rag.indexing.embedder import create_embeddings
from rag.indexing.vector_store import create_vector_store, get_document_count
from rag.prompts.system_prompt import FEASIBILITY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def create_rag_agent():
    load_dotenv()

    embeddings = create_embeddings()
    vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )

    if get_document_count(vector_store) == 0:
        raise RuntimeError(
            "The vector store is empty. Run `uv run python scripts/build_index.py` "
            "before starting the Streamlit app."
        )

    retrieve_context_tool = make_retrieve_context_tool(vector_store)
    tools = [retrieve_context_tool, google_trends]

    model = init_chat_model("gpt-4.1-mini")
    checkpointer_connection = sqlite3.connect("checkpoints.db", check_same_thread=False)
    checkpointer = SqliteSaver(checkpointer_connection)

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=FEASIBILITY_SYSTEM_PROMPT,
        checkpointer=checkpointer,
        response_format=FeasibilityAnalysisResponse,
    )
