from pydantic import ValidationError
import streamlit as st
from app.domain.feasability_form_input import FeasabilityFormInput
from rag.RAG import run_feasibility_analysis

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

    col1, col2 = st.columns(2)

    with col1:
        st.button("Back", on_click=prev_step)

    with col2:
        if st.button("Run RAG Analysis"):
            # TODO: probably in here we have all of the error handling as well?
            result = run_feasibility_analysis(agent, formInput)
            st.success("Send this JSON payload to your RAG backend.")
            # Example:
            # response = requests.post(
            #     "http://localhost:8000/analyze",
            #     json=prompt_payload,
            # )
            # st.write(response.json())
        