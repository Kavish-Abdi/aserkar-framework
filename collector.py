import os
import json
import time
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from crewai import LLM

gemini_model = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def extract_thumbnail(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content", "").startswith("http"):
            return og_image["content"]
            
        twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
        if twitter_image and twitter_image.get("content", "").startswith("http"):
            return twitter_image["content"]
            
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith("http") and 'logo' not in src.lower() and 'icon' not in src.lower():
                return src
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80"

def summarize_article(text):
    # Strip away all raw HTML tags before sending to Gemini
    clean_text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    
    try:
        prompt = (
            "Write a detailed, analytical briefing paragraph (4 to 5 sentences) "
            "explaining the key events, operational impacts, and supply chain risks "
            f"described in this news item: {clean_text[:3000]}"
        )
        response = gemini_model.call([{"role": "user", "content": prompt}])
        return response
    except Exception:
        # If Gemini fails, return the clean text, not raw HTML
        return clean_text[:350] + "..."

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
        # Removed the [:2] limit to get ALL articles
        for entry in feed.entries:
            link = entry.link
            thumbnail = extract_thumbnail(link)
            
            raw_summary = entry.get("summary", entry.get("title", ""))
            summary = summarize_article(raw_summary)
            
            collected_articles.append({
                "title": entry.title,
                "link": link,
                "thumbnail": thumbnail,
                "summary": summary,
                "source": feed.feed.title if hasattr(feed.feed, 'title') else "Industry Intelligence",
                "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # Pause for 4 seconds to prevent getting banned by the Gemini Free Tier
            print(f"Processed: {entry.title[:30]}...")
            time.sleep(4) 
            
    os.makedirs("data", exist_ok=True)
    json_path = "data/intelligence.json"
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                existing_data = json.load(f)
            # Add new articles to the top of the database
            collected_articles = collected_articles + existing_data
        except json.JSONDecodeError:
            pass
            
    with open(json_path, "w") as f:
        json.dump(collected_articles, f, indent=4)
        
    print("Full multi-source intelligence gathered, summarized, and saved.")

if __name__ == "__main__":
    gather_and_store()
