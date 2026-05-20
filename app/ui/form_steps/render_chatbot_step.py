import streamlit as st

from app.utils.bussiness_context_formatter import format_bussiness_context
from app.ui.navigation import prev_step
from rag.RAG import chat_with_rag_agent


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
        text = chat_with_rag_agent(
            agent=agent,
            user_message=user_message,
            business_context=format_bussiness_context(st.session_state.form_data),
            thread_id=st.session_state.chat_thread_id,
        )
    except Exception as exc:
        st.error(f"Chat failed: {exc}")
        return

    st.session_state.chat_history.append({"role": "assistant", "content": text})

    with st.chat_message("assistant"):
        st.markdown(text)
