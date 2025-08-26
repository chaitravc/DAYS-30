# services/news.py

import requests
import os
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_BASE_URL = "https://newsapi.org/v2"


def fetch_top_headlines(country: str = "us", category: str = None, page_size: int = 5) -> Optional[
    List[Dict[str, Any]]]:
    """
    Fetch top headlines from NewsAPI

    Args:
        country: Country code (us, gb, ca, etc.)
        category: Category (business, entertainment, general, health, science, sports, technology)
        page_size: Number of articles to fetch (max 100)

    Returns:
        List of news articles or None if error
    """
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY not found in environment variables")
        return None

    url = f"{NEWS_API_BASE_URL}/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "country": country,
        "pageSize": page_size
    }

    if category:
        params["category"] = category

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "ok":
            return data["articles"]
        else:
            logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return None


def search_news(query: str, sort_by: str = "relevancy", page_size: int = 5) -> Optional[List[Dict[str, Any]]]:
    """
    Search for news articles by query

    Args:
        query: Search query
        sort_by: Sort by relevancy, popularity, or publishedAt
        page_size: Number of articles to fetch

    Returns:
        List of news articles or None if error
    """
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY not found in environment variables")
        return None

    url = f"{NEWS_API_BASE_URL}/everything"
    params = {
        "apiKey": NEWS_API_KEY,
        "q": query,
        "sortBy": sort_by,
        "pageSize": page_size,
        "language": "en"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "ok":
            return data["articles"]
        else:
            logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching news: {e}")
        return None


def format_news_for_llm(articles: List[Dict[str, Any]], max_articles: int = 3) -> str:
    """
    Format news articles for LLM consumption

    Args:
        articles: List of news articles
        max_articles: Maximum number of articles to include

    Returns:
        Formatted string with news summaries
    """
    if not articles:
        return "No recent news articles found."

    formatted_news = "Here are some recent news updates:\n\n"

    for i, article in enumerate(articles[:max_articles], 1):
        title = article.get("title", "No title")
        description = article.get("description", "No description available")
        source = article.get("source", {}).get("name", "Unknown source")

        formatted_news += f"{i}. **{title}**\n"
        formatted_news += f"   Source: {source}\n"
        formatted_news += f"   Summary: {description}\n\n"

    return formatted_news


def should_fetch_news(user_query: str) -> bool:
    """
    Determine if the user query is asking for news or current events

    Args:
        user_query: User's input query

    Returns:
        Boolean indicating if news should be fetched
    """
    news_keywords = [
        "news", "latest", "recent", "current", "today", "happening",
        "update", "events", "headlines", "breaking", "what's new",
        "tell me about", "what happened", "any news"
    ]

    query_lower = user_query.lower()
    return any(keyword in query_lower for keyword in news_keywords)

