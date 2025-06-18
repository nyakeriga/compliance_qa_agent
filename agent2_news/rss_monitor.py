import feedparser

# Trusted healthcare/compliance-related RSS feeds
RSS_FEEDS = [
    "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
    "https://www.npr.org/rss/rss.php?id=1001",
    "https://www.reutersagency.com/feed/?best-topics=healthcare",
]

def fetch_latest_news():
    headlines = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:10]:  # Limit to latest 10 articles per feed
            headlines.append({
                "title": entry.title,
                "url": entry.link,
                "summary": entry.get("summary", ""),
            })
    return headlines
