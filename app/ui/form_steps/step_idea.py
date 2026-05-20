from pydantic import ValidationError
import streamlit as st

from app.domain.idea_input import IdeaInput
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

            raw_idea_data = {
                "one_sentence_pitch": pitch,
                "problem_solved": problem,
                "target_users": target_users,
                "target_countries": split_comma_text(countries),
            }
            
            try:
                idea_input = IdeaInput.model_validate(raw_idea_data)
            except ValidationError as e:
                for err in e.errors():
                    loc = err.get("loc", ())
                    message = err["msg"]

                    if message.startswith("Value error, "):
                        message = message.removeprefix("Value error, ")

                    if loc:
                        st.error(f"{loc[0]}: {message}")
                    else:
                        st.error(message)

                return
            
            st.session_state.form_data["idea"] = idea_input.model_dump()
            next_step()
            st.rerun()
