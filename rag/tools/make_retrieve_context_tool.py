from langchain.tools import tool
from langchain_community.vectorstores import Chroma

# TODO: transfer into a separate tool because this is used to retrieve data from a similarity store
def make_retrieve_context_tool(vector_store : Chroma):
    
    @tool(response_format="content_and_artifact")
    # TODO: Better let's retrieve chunks until a certain similarity cutoff
    def retrieve_context(query: str):
        """Retrieve information to help answer a query."""
        retrieved_docs = vector_store.similarity_search(query, k=4)
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}"
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs

    return retrieve_context