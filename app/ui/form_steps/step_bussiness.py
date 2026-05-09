import streamlit as st

from app.ui.navigation import next_step, prev_step
from app.utils.text_helpers import split_comma_text


def render_business_step() -> None:
    data = st.session_state.form_data

    st.subheader("Business feasibility")

    with st.form("business_form"):
        monetization_options = [
            "Subscription",
            "Freemium",
            "Ads",
            "One-time purchase",
            "In-app purchases",
            "Marketplace fee",
            "Not sure",
        ]
        saved_model = data["business"].get("monetization_model", "Not sure")
        monetization_index = (
            monetization_options.index(saved_model)
            if saved_model in monetization_options
            else len(monetization_options) - 1
        )

        monetization_model = st.selectbox(
            "Monetization model",
            monetization_options,
            index=monetization_index,
        )

        expected_price = st.text_input(
            "Expected price",
            value=data["business"].get("expected_price", ""),
            placeholder="Example: EUR 4.99/month",
        )

        paid_features = st.text_area(
            "What would users pay for?",
            value=", ".join(data["business"].get("paid_features", [])),
            placeholder="Example: unlimited usage, premium filters, AI recommendations",
        )

        competitors = st.text_area(
            "Known competitors",
            value=", ".join(data["business"].get("known_competitors", [])),
            placeholder="Example: Duolingo, Notion, Calm",
        )

        differentiation = st.text_area(
            "Why would users choose your app instead?",
            value=data["business"].get("differentiation", ""),
            placeholder="Example: It focuses only on Lithuanian students and shows real-time availability.",
        )

        budget = st.text_input(
            "Build budget",
            value=data["business"].get("budget", ""),
            placeholder="Example: EUR 2,000",
        )

        timeline = st.text_input(
            "Timeline",
            value=data["business"].get("timeline", ""),
            placeholder="Example: 3 months",
        )

        team_size = st.number_input(
            "Team size",
            min_value=1,
            max_value=50,
            value=data["business"].get("team_size", 1),
        )

        submitted = st.form_submit_button("Save and review")

        if submitted:
            if not differentiation:
                st.error("Differentiation is required.")
                return

            data["business"] = {
                "monetization_model": monetization_model,
                "expected_price": expected_price,
                "paid_features": split_comma_text(paid_features),
                "known_competitors": split_comma_text(competitors),
                "differentiation": differentiation,
                "budget": budget,
                "timeline": timeline,
                "team_size": team_size,
            }
            next_step()
            st.rerun()

    st.button("Back", on_click=prev_step)
