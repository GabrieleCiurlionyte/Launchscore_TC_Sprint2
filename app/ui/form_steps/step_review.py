from pydantic import ValidationError
import streamlit as st
from app.domain.input.feasability_form_input import FeasabilityFormInput
from app.ui.navigation import prev_step

def render_review_step(agent) -> None:
    raw_data = st.session_state.form_data

    try:
        formInput = FeasabilityFormInput.model_validate(raw_data)
    except ValidationError as e:
        st.error("Please fix the form data before running the analysis.")
        st.json(e.errors())
        return
    
    st.subheader("Structured RAG Input")
    st.json(formInput)

    col1, spacer, col2 = st.columns([1, 5, 1])

    with col1:
        st.button("Back", on_click=prev_step)

    with col2:
        if st.button("Open Chatbot"):
            st.session_state.analysis_error = None
            st.session_state.step = 4
            st.rerun()
                
    if st.session_state.analysis_error:
        st.error(st.session_state.analysis_error)


        
