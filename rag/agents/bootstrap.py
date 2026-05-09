import logging
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite import SqliteSaver

from app.domain.feasibility_analysis_response import FeasibilityAnalysisResponse
from rag.tools.make_retrieve_context_tool import make_retrieve_context_tool
from rag.tools.googleTrends.googleTrendsTool import google_trends
from rag.indexing.embedder import create_embeddings
from rag.indexing.index_documents import index_pdf_documents
from rag.indexing.vector_store import create_vector_store
from rag.prompts.system_prompt import FEASIBILITY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

def create_rag_agent():
    load_dotenv()

    embeddings = create_embeddings()
    vector_store = create_vector_store(
        embeddings=embeddings,
        persist_directory="./chroma_langchain.db",
    )

    pdf_path = Path("data/raw_pdfs/sensor_tower__state_of_mobile_2026__en.pdf")
    index_pdf_documents(vector_store=vector_store, pdf_path=pdf_path)

    retrieve_context_tool = make_retrieve_context_tool(vector_store)
    tools = [retrieve_context_tool, google_trends]

    model = init_chat_model("gpt-4.1-mini")
    checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

    return create_agent(
        model=model,
        tools=tools,
        system_prompt=FEASIBILITY_SYSTEM_PROMPT,
        checkpointer=checkpointer,
        response_format=FeasibilityAnalysisResponse,
    )