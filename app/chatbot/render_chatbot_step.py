import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

from app.chatbot.prompts.chatbot_prompt import CHATBOT_PROMPT
from app.utils.bussiness_context_formatter import format_bussiness_context
from rag.indexing.config import DEFAULT_CHAT_MODEL
from app.ui.navigation import prev_step


def render_chatbot_step() -> None:
    st.subheader("Business Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if st.button("Back", on_click=prev_step):
        return

    model = init_chat_model(DEFAULT_CHAT_MODEL, temperature=0.2)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         f"{CHATBOT_PROMPT}."
         "{business_context}"),
        ("placeholder", "{history}"),
        ("human", "{user_message}"),
    ])

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_message = st.chat_input("Ask about risks, pricing, GTM, competition...")
    if not user_message:
        return

    st.session_state.chat_history.append({"role": "user", "content": user_message})

    history = []
    for msg in st.session_state.chat_history[:-1]:
        history.append(("human" if msg["role"] == "user" else "ai", msg["content"]))

    response = (prompt | model).invoke({
        "business_context": format_bussiness_context(st.session_state.form_data),
        "history": history,
        "user_message": user_message,
    })

    text = response.content if hasattr(response, "content") else str(response)
    st.session_state.chat_history.append({"role": "assistant", "content": text})

    with st.chat_message("assistant"):
        st.markdown(text)