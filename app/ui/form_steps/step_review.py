import json
import streamlit as st

from app.ui.navigation import prev_step


def render_review_step() -> None:
    data = st.session_state.form_data

    st.subheader("Structured RAG Input")
    st.json(data)

    prompt_payload = build_prompt_payload(data)

    st.subheader("Prompt Payload")
    st.code(json.dumps(prompt_payload, indent=2), language="json")

    col1, col2 = st.columns(2)

    with col1:
        st.button("Back", on_click=prev_step)

    with col2:
        if st.button("Run RAG Analysis"):
            st.success("Send this JSON payload to your RAG backend.")
            # Example:
            # response = requests.post(
            #     "http://localhost:8000/analyze",
            #     json=prompt_payload,
            # )
            # st.write(response.json())
            
def build_prompt_payload(data: dict) -> dict:
    return {
        "task": "Analyze mobile app idea feasibility and profitability.",
        "input": data,
        "required_output": {
            "feasibility_score": "0-100",
            "profitability_score": "0-100",
            "market_demand": "analysis with evidence",
            "competition": "analysis with competitor references",
            "monetization": "recommendation",
            "risks": "ranked list",
            "mvp_scope": "recommended MVP features",
            "go_no_go": "Go | No-go | Needs validation",
        },
    }
