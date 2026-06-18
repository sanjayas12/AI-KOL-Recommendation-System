import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI KOL Recommendation System",
    layout="wide"
)

st.title("🔬 AI KOL Recommendation System")

st.markdown(
    "Discover top researchers using Semantic Search, Hybrid Ranking and AI-generated recommendations."
)

query = st.text_input(
    "Enter Research Domain",
    placeholder="Computer Vision"
)

if st.button("Search Researcher"):

    with st.spinner("Finding Best Researchers..."):

        response = requests.post(
            "http://127.0.0.1:8000/ai-recommend-v2",
            params={"query": query}
        )

        data = response.json()

        st.success("Recommendation Generated")

        # Top Researcher
        st.subheader("🏆 Top Recommended Researcher")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Researcher",
                data["top_researcher"]
            )

            st.metric(
                "Citations",
                data["citations"]
            )

        with col2:
            st.metric(
                "H Index",
                data["h_index"]
            )

        # AI Summary
        st.subheader("🤖 AI Explanation")

        st.info(
            data["ai_summary"]
        )

        # Top 5 Recommendations
        st.subheader("📊 Top 5 Recommended Researchers")

        recommendations = pd.DataFrame(
            data["recommendations"]
        )

        st.dataframe(
            recommendations,
            use_container_width=True
        )