import logging

logger = logging.getLogger(__name__)

def chat_with_rag_agent(agent, user_message: str, business_context: str, thread_id: str) -> str:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Business context:\n"
                    f"{business_context}\n\n"
                    "User question:\n"
                    f"{user_message}"
                ),
            }
        ]
    }
    logger.info("Agent payload: %s", payload)

    response = agent.invoke(
        payload,
        config={"configurable": {"thread_id": thread_id}}
    )

    logger.info("Agent response: %s", response)
    messages = response.get("messages", [])
    if not messages:
        raise RuntimeError("RAG agent returned no messages.")

    last_message = messages[-1]
    content = getattr(last_message, "content", last_message)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = [
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        ]
        text = "\n".join(part for part in text_parts if part).strip()
        if text:
            return text

    return str(content)
