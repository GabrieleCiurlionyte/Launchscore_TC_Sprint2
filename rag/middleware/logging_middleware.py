import logging
from typing import Callable

from langchain.agents.middleware import before_agent, after_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command

logger = logging.getLogger(__name__)

@before_agent
def log_rag_start(state, runtime):
    logger.info("RAG agent started")
    messages = state.get("messages", [])
    if messages:
        logger.info("Last user message: %s", messages[-1])

@after_agent
def log_rag_end(state, runtime):
    logger.info("RAG agent finished")
    
@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    tool_name = request.tool_call["name"]
    tool_args = request.tool_call.get("args", {})

    logger.info(f"Executing tool: {tool_name} with arguments: {tool_args}")

    try:
        result = handler(request)
        logger.info("Tool completed: %s", tool_name)
        
        if isinstance(result, ToolMessage):
            logger.info(f"Tool {tool_name} result: {result.content}")
        
        return result
    except Exception as exc:
        logger.exception("Tool failed: %s | error: %s", tool_name, exc)
        raise