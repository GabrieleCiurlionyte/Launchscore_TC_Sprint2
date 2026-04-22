from langchain.tools import tool
from langchain_chroma import Chroma
from langgraph.config import get_stream_writer

@tool(response_format="content_and_artifact")
def retrieve_context(vector_store: Chroma, query: str):
    """Retrieve information to help answer a query."""
    
    writer = get_stream_writer()
    
    writer(f"Lookup content from the vector store for query: {query}")
    
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    writer(f"Retrieved results from vector store: {serialized}")
    return serialized, retrieved_docs