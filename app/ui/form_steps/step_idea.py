import streamlit as st

from app.ui.navigation import next_step
from app.utils.text_helpers import split_comma_text

def render_idea_step() -> None:
    data = st.session_state.form_data

    st.subheader("Describe the app idea")

    with st.form("idea_form"):
        pitch = st.text_area(
            "One-sentence pitch",
            value=data["idea"].get("one_sentence_pitch", ""),
            placeholder="Example: An app that helps students find quiet study places nearby.",
        )

        problem = st.text_area(
            "What problem does it solve?",
            value=data["idea"].get("problem_solved", ""),
            placeholder="Example: Students waste time searching for quiet and available places to study.",
        )

        target_users = st.text_input(
            "Target users",
            value=data["idea"].get("target_users", ""),
            placeholder="Example: University students in Vilnius",
        )

        countries = st.text_input(
            "Target countries / regions",
            value=", ".join(data["idea"].get("target_countries", [])),
            placeholder="Example: Lithuania, Poland, Germany",
        )

        submitted = st.form_submit_button("Save and continue")

        if submitted:
            if not pitch or not problem or not target_users:
                st.error("Pitch, problem, and target users are required.")
                return

            data["idea"] = {
                "one_sentence_pitch": pitch,
                "problem_solved": problem,
                "target_users": target_users,
                "target_countries": split_comma_text(countries),
                "category": {
                    "mode": "auto",
                    "inferred_primary": None,
                    "inferred_related": [],
                },
            }
            next_step()
            st.rerun()
