import os
import json
import feedparser

def gather_and_store():
    rss_urls = [
        "https://news.google.com/rss/search?q=railway+infrastructure+delays+india",
        "https://news.google.com/rss/search?q=packaged+foods+sector+supply+chain"
    ]
    
    collected_articles = []
    
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        for entry in feed.entries[:3]:
            collected_articles.append({
                "title": entry.title,
                "summary": entry.summary,
                "published": getattr(entry, 'published', 'Recently')
            })
            
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Save directly to a local JSON file (this gets committed back to GitHub)
    with open("data/intelligence.json", "w") as f:
        json.dump(collected_articles, f, indent=4)
        
    print("Background collection complete. Data saved to data/intelligence.json.")

if __name__ == "__main__":
    gather_and_store()
