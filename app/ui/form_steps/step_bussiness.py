from pydantic import ValidationError
import streamlit as st

from app.ui.navigation import next_step, prev_step
from app.utils.text_helpers import split_comma_text
from app.domain.bussiness_input import BusinessInput


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

        expected_price_eur = st.number_input(
            "Expected price (EUR)",
            min_value=0.0,
            value=float(data["business"].get("expected_price_eur", 0.0)),
            step=1.0,
            help="Use 0 if the app will be free at launch.",
        )

        billing_period_options = ["Monthly", "Yearly", "One-time", "Free", "Not sure"]
        saved_billing_period = data["business"].get(
            "expected_price_period",
            "Not sure",
        )
        billing_period_index = (
            billing_period_options.index(saved_billing_period)
            if saved_billing_period in billing_period_options
            else len(billing_period_options) - 1
        )

        expected_price_period = st.selectbox(
            "Price period",
            billing_period_options,
            index=billing_period_index,
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

        build_budget_eur = st.number_input(
            "Build budget (EUR)",
            min_value=0,
            value=int(data["business"].get("build_budget_eur", 0)),
            step=500,
        )

        timeline_months = st.number_input(
            "Timeline (months)",
            min_value=1,
            value=int(data["business"].get("timeline_months", 3)),
            step=1,
        )

        team_size = st.number_input(
            "Team size",
            min_value=1,
            max_value=50,
            value=data["business"].get("team_size", 1),
        )

        submitted = st.form_submit_button("Save and review")

        if submitted:
            raw_business_data = {
                "monetization_model": monetization_model,
                "expected_price_eur": expected_price_eur,
                "expected_price_period": expected_price_period,
                "paid_features": split_comma_text(paid_features),
                "known_competitors": split_comma_text(competitors),
                "differentiation": differentiation,
                "build_budget_eur": build_budget_eur,
                "timeline_months": timeline_months,
                "team_size": team_size,
            }

            try:
                business_input = BusinessInput.model_validate(raw_business_data)
            except ValidationError as e:
                for err in e.errors():
                    loc = err.get("loc", ())
                    message = err["msg"]

                if message.startswith("Value error, "):
                    message = message.removeprefix("Value error, ")

                if loc:
                    field_path = ".".join(str(part) for part in loc)
                    st.error(f"{field_path}: {message}")
                else:
                    st.error(message)
                return

            st.session_state.form_data["business"] = business_input.model_dump()
            next_step()
            st.rerun()

    st.button("Back", on_click=prev_step)
