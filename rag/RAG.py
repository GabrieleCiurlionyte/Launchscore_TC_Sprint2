import logging
import streamlit as st

logger = logging.getLogger(__name__)

def run_agent_with_event_streaming(agent, user_message: str, business_context: str, thread_id: str) -> str:
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
    
    tool_results = []
    final_text = ""

    stream = agent.stream_events(
        payload,
        config={"configurable": {"thread_id": thread_id}},
        version="v3",
    )
    
    with st.status("Running agent...", expanded=True) as status:
        for message in stream.messages:
            status.write(f"Model node: {message.node}")

            finalized_tool_calls = message.tool_calls.get()
            if finalized_tool_calls:
                status.write(f"Finalized tool calls: {finalized_tool_calls}")

            text_parts = []
            for delta in message.text:
                text_parts.append(delta)

            if text_parts:
                partial_text = "".join(text_parts)
                status.write(partial_text)

            full_message = message.output
            if full_message and getattr(full_message, "content", None):
                content = full_message.content
                if isinstance(content, str):
                    final_text = content
                elif isinstance(content, list):
                    final_text = "\n".join(
                        part.get("text", "")
                        for part in content
                        if isinstance(part, dict) and part.get("type") == "text"
                    ).strip()

        for call in stream.tool_calls:
            status.write(f"Running tool: {call.tool_name}")
            status.write(f"Input: {call.input}")

            output_chunks = []
            for delta in call.output_deltas:
                output_chunks.append(str(delta))

            tool_result = {
                "tool_name": call.tool_name,
                "input": call.input,
                "output": call.output if call.output is not None else "".join(output_chunks),
                "error": call.error,
            }
            tool_results.append(tool_result)

            if call.error:
                status.write(f"Tool error: {call.error}")
            else:
                status.write(f"Tool output: {tool_result['output']}")

        status.update(label="Agent complete", state="complete")

    final_state = stream.output
    return final_text, tool_results, final_state
