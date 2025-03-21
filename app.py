import streamlit as st
import requests

# Streamlit Web Application Title
st.title("📰 News Sentiment & Text-to-Speech Analysis")

# Input field for the company name
company = st.text_input("Enter Company Name", placeholder="e.g., Tesla, Apple, Google")

if st.button("Analyze News"):
    with st.spinner("Fetching news..."):
        response = requests.post("http://127.0.0.1:5000/get_news", json={"company": company})
        if response.status_code == 200:
            data = response.json()

            # ✅ Display News Articles First
            st.subheader("📰 News Articles")
            for article in data["articles"]:
                st.write(f"**[{article['title']}]({article['link']})**")  # Clickable link
                st.write(f"📜 {article['summary']}")
                st.write(f"**Sentiment:** {article['sentiment']}")
                st.write(f"**Topics:** {', '.join(article['topics'])}")
                st.markdown("---")

            # ✅ Play Audio Summary
            if "audio" in data and data["audio"]:
                st.subheader("🔊 Listen to Summary")
                st.audio(data["audio"])

            # ✅ After News & Audio → Show Sentiment Analysis
            st.subheader("📊 Sentiment Analysis Results")

            # ✅ Display Sentiment Summary
            st.write("### 📝 Sentiment Summary")
            st.json(data["sentiment_summary"])

            # ✅ Display Comparative Sentiment Score
            st.write("### 🔍 Comparative Sentiment Score")
            st.json(data["comparative_analysis"])

            # ✅ Display Topics Extracted
            st.write("### 🔑 Topics Extracted")
            st.write(", ".join(data["topics"]))

        else:
            st.error("Failed to fetch news. Try again later.")
