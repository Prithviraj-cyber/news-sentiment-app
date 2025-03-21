import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
from gtts import gTTS
import os
import html

# Function to fetch news articles from Google News RSS
def get_news(company):
    """Fetches and cleans news articles from Google News RSS."""
    rss_url = f"https://news.google.com/rss/search?q={company}&hl=hi-IN&gl=IN&ceid=IN:hi"
    response = requests.get(rss_url)

    if response.status_code != 200:
        return []  # Return empty list if request fails

    soup = BeautifulSoup(response.content, 'xml')
    articles = []

    for item in soup.find_all('item')[:10]:
        title = item.title.text.strip()
        summary = re.sub(r'<.*?>', '', item.description.text).strip()
        link = item.link.text.strip()

        articles.append({
            "title": title, 
            "summary": summary, 
            "link": link
        })

    return articles if articles else [{"title": "No news found", "summary": "", "link": ""}]


# Function to perform sentiment analysis
def analyze_sentiment(text):
    """Determines sentiment category based on text polarity."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
    
# function to perform audio clear
def clean_text_for_tts(text):
    """Removes unwanted HTML entities like &nbsp; before converting to speech."""
    text = html.unescape(text)  # Convert &nbsp; and other entities to normal text
    text = text.replace("\n", " ")  # Remove new lines
    text = text.replace("  ", " ")  # Remove extra spaces
    return text.strip()

# Function to convert text summary into Hindi speech
def text_to_speech(text, filename="static/output.mp3"):
    """Converts cleaned text into Hindi speech."""
    text = clean_text_for_tts(text)  # Apply cleaning before conversion
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    return filename
