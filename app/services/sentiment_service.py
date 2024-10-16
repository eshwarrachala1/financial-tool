# app/services/sentiment_service.py

import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from app.config import settings

# Initialize the VADER sentiment analyzer
nltk.download('vader_lexicon')
vader_analyzer = SentimentIntensityAnalyzer()

# You can use a news API like NewsAPI, but we'll mock the news data for now.
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"

def fetch_recent_news(symbol: str):
    """
    Fetch recent news articles about the stock using NewsAPI.
    You can also replace this function with any other news provider.
    """
    params = {
        "q": symbol,
        "apiKey": settings.NEWS_API_KEY,
        "sortBy": "publishedAt",
        "language": "en"
    }

    response = requests.get(NEWS_API_BASE_URL, params=params)
    news_data = response.json()

    if "articles" in news_data:
        return [article['title'] for article in news_data['articles'][:15]]  # Get top 5 article titles
    else:
        return []

def analyze_sentiment(text: str):
    """
    Analyze the sentiment of a given text using VADER.
    Returns a sentiment score: positive, neutral, or negative.
    """
    sentiment_scores = vader_analyzer.polarity_scores(text)
    if sentiment_scores['compound'] >= 0.05:
        return "positive"
    elif sentiment_scores['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

def get_stock_sentiment(symbol: str):
    """
    Fetch recent news for the given stock symbol and analyze the sentiment.
    """
    news_titles = fetch_recent_news(symbol)

    if not news_titles:
        return {"symbol": symbol, "sentiment": "neutral", "message": "No recent news found"}

    # Analyze the sentiment of the news titles
    sentiments = [analyze_sentiment(title) for title in news_titles]

    # Count the positive, neutral, and negative sentiments
    positive_count = sentiments.count("positive")
    negative_count = sentiments.count("negative")
    neutral_count = sentiments.count("neutral")

    # Determine overall sentiment based on majority
    if positive_count > negative_count:
        overall_sentiment = "positive"
    elif negative_count > positive_count:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"

    return {
        "symbol": symbol,
        "sentiment": overall_sentiment,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "news_titles": news_titles  # Return the analyzed news for transparency
    }
