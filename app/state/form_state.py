import streamlit as st

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
