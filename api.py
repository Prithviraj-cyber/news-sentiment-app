from flask import Flask, request, jsonify
from utils import get_news, analyze_sentiment, text_to_speech
import re
from collections import Counter
import yake

# Initialize Flask API
app = Flask(__name__)

def extract_topics(text):
    """Extracts meaningful keywords using YAKE (Yet Another Keyword Extractor)."""
    kw_extractor = yake.KeywordExtractor(lan="hi", n=2, dedupLim=0.9, top=5)
    keywords = kw_extractor.extract_keywords(text)
    return [word[0] for word in keywords]

@app.route('/get_news', methods=['POST'])
def get_news_data():
    """Fetches news, performs sentiment analysis, extracts topics, and generates speech."""
    data = request.get_json()
    company = data.get("company", "Tesla")  # Get company name from request
    articles = get_news(company)  # Fetch news articles related to the company

    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    all_topics = []
    summary_texts = []

    for article in articles:
        # Perform sentiment analysis on the article summary
        article["sentiment"] = analyze_sentiment(article["summary"])
        sentiment_counts[article["sentiment"]] += 1
        summary_texts.append(article["summary"])

        # Extract topics from article title
        article["topics"] = extract_topics(article["title"])
        all_topics.extend(article["topics"])

    # Count topic frequency and extract top topics
    topic_freq = Counter(all_topics)
    top_topics = [word for word, _ in topic_freq.most_common(5)]

    # Generate comparative sentiment analysis
    comparative_analysis = {
        "Sentiment Distribution": sentiment_counts,
        "Coverage Differences": [
            {
                "Comparison": "Some articles focus on positive financial growth, while others highlight challenges.",
                "Impact": "Investors may react positively to good news but remain cautious about risks."
            }
        ],
        "Topic Overlap": {
            "Common Topics": list(set(all_topics)),
            "Unique Topics in Articles": list(set(top_topics))
        }
    }

    # Convert the summarized news content into Hindi speech
    formatted_text = ". ".join(summary_texts)
    audio_file = text_to_speech(formatted_text)

    return jsonify({
        "articles": articles,
        "sentiment_summary": sentiment_counts,
        "comparative_analysis": comparative_analysis,
        "topics": top_topics,
        "audio": audio_file
    })

if __name__ == '__main__':
    app.run(debug=True)
