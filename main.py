import streamlit as st

from app.state.form_state import init_form_state
from app.ui.form_steps.step_bussiness import render_business_step
from app.ui.form_steps.step_idea import render_idea_step
from app.ui.form_steps.step_market import render_market_step
from app.ui.form_steps.step_review import render_review_step

STEPS = ["Idea", "Market", "Business", "Review"]

st.set_page_config(page_title="App Idea Feasibility Wizard", layout="centered")


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
else:
    render_review_step()
