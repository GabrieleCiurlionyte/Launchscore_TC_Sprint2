import streamlit as st

from app.ui.navigation import next_step, prev_step
from app.utils.text_helpers import split_comma_text


def render_market_step() -> None:
    data = st.session_state.form_data

    st.subheader("Validate demand")

    with st.form("market_form"):
        pain_intensity = st.slider(
            "How painful is this problem?",
            min_value=1,
            max_value=10,
            value=data["market"].get("pain_intensity", 5),
            help="1 = minor inconvenience, 10 = urgent painful problem.",
        )

        frequency_options = ["Daily", "Weekly", "Monthly", "Rarely"]
        saved_frequency = data["market"].get("how_often_user_has_problem", "Weekly")
        frequency_index = (
            frequency_options.index(saved_frequency)
            if saved_frequency in frequency_options
            else 1
        )

        frequency = st.selectbox(
            "How often does the target user experience this problem?",
            frequency_options,
            index=frequency_index,
        )

        alternatives = st.text_area(
            "What do users currently use instead?",
            value=", ".join(data["market"].get("current_alternatives", [])),
            placeholder="Example: Google Maps, Excel, WhatsApp groups, existing apps",
        )

        payment_options = ["Yes", "No", "Not sure"]
        saved_payment = data["market"].get("is_problem_paid_for_today", "Not sure")
        payment_index = (
            payment_options.index(saved_payment)
            if saved_payment in payment_options
            else 2
        )

        existing_payment = st.radio(
            "Do users already pay to solve this problem?",
            payment_options,
            index=payment_index,
            horizontal=True,
        )

        submitted = st.form_submit_button("Save and continue")

        if submitted:
            data["market"] = {
                "pain_intensity": pain_intensity,
                "how_often_user_has_problem": frequency,
                "current_alternatives": split_comma_text(alternatives),
                "is_problem_paid_for_today": existing_payment,
            }
            next_step()
            st.rerun()

    st.button("Back", on_click=prev_step)
