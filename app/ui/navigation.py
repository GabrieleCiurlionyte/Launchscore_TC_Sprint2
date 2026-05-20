import streamlit as st

def next_step(total_steps: int = 4) -> None:
    st.session_state.step = min(st.session_state.step + 1, total_steps - 1)

def prev_step() -> None:
    st.session_state.step = max(st.session_state.step - 1, 0)
