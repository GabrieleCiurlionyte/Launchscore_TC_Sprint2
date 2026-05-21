import streamlit as st

from app.utils.bussiness_context_formatter import format_bussiness_context
from app.ui.navigation import prev_step
from rag.RAG import run_agent_with_event_streaming
from rag.guardrails.chat_message_validator import ChatMessageValidationError


def render_chatbot_step(agent) -> None:
    st.subheader("Business Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Back", on_click=prev_step):
        return

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_message = st.chat_input("Ask about risks, pricing, GTM, competition...")
    if not user_message:
        return

    st.session_state.chat_history.append({"role": "user", "content": user_message})

    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        final_text, tool_results, final_state = run_agent_with_event_streaming(
            agent=agent,
            user_message=user_message,
            business_context=format_bussiness_context(st.session_state.form_data),
            thread_id=st.session_state.chat_thread_id,
)
    except ChatMessageValidationError as exc:
        assistant_message = str(exc)
        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_message}
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_message)

        return
    except Exception as exc:
        st.session_state.chat_history.pop()
        st.error(f"Chat failed: {exc}")
        return

    st.session_state.chat_history.append(
    {"role": "assistant", "content": final_text or "No response returned."}
)

    with st.chat_message("assistant"):
        st.markdown(final_text or "No response returned.")
        
        if tool_results:
            with st.expander("Evidence used"):
                for result in tool_results:
                    st.write(f"Tool: {result['tool_name']}")
                    if result.get("error"):
                        st.error(result["error"])
                    else:
                        st.write(result["summary"])
