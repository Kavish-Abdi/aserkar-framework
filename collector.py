import os
import json
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from crewai import LLM

# Initialize Gemini for summarization
gemini_model = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def extract_thumbnail(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", property="og:image")
        if og_image:
            return og_image["content"]
        for img in soup.find_all('img'):
            if img.get('src') and 'logo' not in img['src'].lower():
                return img['src']
    except:
        pass
    return "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80" 

def summarize_article(text):
    try:
        prompt = f"Provide a strict 2-sentence executive summary of the following supply chain news focusing on risks and trends: {text[:2000]}"
        response = gemini_model.call([{"role": "user", "content": prompt}])
        return response
    except Exception:
        return text[:200] + "..."

def gather_and_store():
    rss_urls = [
        "https://www.supplychainbrain.com/rss",
        "https://feeds.feedburner.com/logisticsmgmt/latest",
        "https://procureinsights.com/feed/",
        "https://news.google.com/rss/search?q=wall+street+journal+supply+chain+logistics"
    ]
    
    collected_articles = []
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        for entry in feed.entries[:2]:
            link = entry.link
            thumbnail = extract_thumbnail(link)
            summary = summarize_article(entry.summary)
            
            collected_articles.append({
                "title": entry.title,
                "link": link,
                "thumbnail": thumbnail,
                "summary": summary,
                "source": feed.feed.title if hasattr(feed.feed, 'title') else "Industry Source",
                "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
    os.makedirs("data", exist_ok=True)
    json_path = "data/intelligence.json"
    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            existing_data = json.load(f)
        collected_articles = existing_data + collected_articles
        
    with open(json_path, "w") as f:
        json.dump(collected_articles, f, indent=4)
        
    print("Multi-source intelligence gathered, summarized, and backed up.")

if __name__ == "__main__":
    gather_and_store()
