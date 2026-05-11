import streamlit as st
import uuid

DEFAULT_DATA = {
    "idea": {},
    "market": {},
    "business": {},
}

def init_form_state() -> None:
    if "step" not in st.session_state:
        st.session_state.step = 0

    if "form_data" not in st.session_state:
        st.session_state.form_data = DEFAULT_DATA.copy()

    if "analysis_thread_id" not in st.session_state:
        st.session_state.analysis_thread_id = str(uuid.uuid4())
