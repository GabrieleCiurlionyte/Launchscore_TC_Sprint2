import streamlit as st

def render_result_step() -> None:
    result = st.session_state.get("analysis_result")

    if result is None:
        st.warning("No feasibility analysis result is available yet.")
        if st.button("Back to Review"):
            st.session_state.step = 3
            st.rerun()
        return

    if hasattr(result, "model_dump"):
        result_data = result.model_dump()
    else:
        result_data = result

    decision = result_data.get("go_or_no_go_decision", "unknown")
    score = result_data.get("profitability_score", "N/A")

    st.subheader("Feasibility Analysis Result")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Profitability Score", score)
    with col2:
        st.metric("Decision", str(decision).replace("-", " ").title())

    st.markdown("### Market Risk Analysis")
    st.write(result_data.get("market_risk_analysis", "No analysis available."))

    st.markdown("### Competitor Summary")
    st.write(result_data.get("competitor_summary", "No summary available."))

    st.markdown("### MVP Recommendation")
    st.write(result_data.get("mvp_recommendation", "No recommendation available."))

    st.markdown("### Monetization Recommendation")
    st.write(result_data.get("monetization_recommendation", "No recommendation available."))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Review"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("Run Again"):
            st.session_state.step = 3
            st.rerun()
