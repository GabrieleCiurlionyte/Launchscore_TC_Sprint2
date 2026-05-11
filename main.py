import streamlit as st
import logging
import copy
from app.state.form_state import init_form_state
from app.ui.form_steps.step_bussiness import render_business_step
from app.ui.form_steps.step_idea import render_idea_step
from app.ui.form_steps.step_market import render_market_step
from app.ui.form_steps.step_review import render_review_step
from app.ui.form_steps.step_result import render_result_step
from rag.agents.bootstrap import create_rag_agent
from scripts.preset_form_data import PRESET_FORM_DATA

logging.basicConfig(level=logging.INFO)

# TODO: thesse steps maybe should be an enum and transferred somewhere else
STEPS = ["Idea", "Market", "Business", "Review", "Result"]

st.set_page_config(page_title="App Idea Feasibility Calculator", layout="centered")

@st.cache_resource
def get_rag_agent():
    return create_rag_agent()

with st.sidebar:
    if st.button("Load Demo Preset"):
        st.session_state.form_data = copy.deepcopy(PRESET_FORM_DATA)
        st.session_state.step = 3
        st.rerun()

def render_progress_header() -> None:
    st.title("App Idea Feasibility Wizard")
    st.progress((st.session_state.step + 1) / len(STEPS))
    st.caption(
        f"Step {st.session_state.step + 1} of {len(STEPS)}: "
        f"{STEPS[st.session_state.step]}"
    )

init_form_state()
render_progress_header()

step = st.session_state.step

if step == 0:
    render_idea_step()
elif step == 1:
    render_market_step()
elif step == 2:
    render_business_step()
elif step == 3:
    try:
        rag_agent = get_rag_agent()
    except RuntimeError as exc:
        st.error(str(exc))
        st.stop()
    render_review_step(rag_agent)
elif step == 4:
    render_result_step()
else:
    st.error("Invalid program state")
    
