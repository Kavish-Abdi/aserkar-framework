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

# The Professor's Disruption Matrix
RISK_CATEGORIES = {
    "Geopolitics & Trade": ["tariff", "export control", "quota", "sanction", "embargo", "trade restriction", "customs delay", "protectionism", "war", "military", "blockade", "piracy", "red sea", "terrorism", "border closure", "protest", "riot", "coup", "shutdown", "civil unrest"],
    "Natural Disasters": ["typhoon", "hurricane", "cyclone", "blizzard", "heatwave", "freeze", "earthquake", "tsunami", "volcanic", "flood", "landslide", "drought", "canal draft", "wildfire", "water scarcity"],
    "Logistics & Infrastructure": ["port congestion", "route closure", "canal blockage", "airspace restriction", "derailment", "trucking shortage", "cyberattack", "ransomware", "outage", "blackout", "container shortage", "vessel delay", "blank sailing", "warehousing capacity"],
    "Labor & Economics": ["strike", "union", "worker shortage", "walkout", "lockout", "bankruptcy", "hyperinflation", "devaluation", "price spike", "liquidity crisis"],
    "Public Health & Safety": ["pandemic", "epidemic", "outbreak", "quarantine", "lockdown", "factory fire", "chemical spill", "hazardous", "recall"]
}

def extract_thumbnail(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content", "").startswith("http"):
            return og_image["content"]
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80"

def check_risk_triggers(text):
    text_lower = text.lower()
    triggered_categories = []
    for category, keywords in RISK_CATEGORIES.items():
        if any(keyword in text_lower for keyword in keywords):
            triggered_categories.append(category)
    return triggered_categories

def summarize_article(text, categories):
    clean_text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    cats_str = ", ".join(categories)
    
    try:
        prompt = (
            f"You are a global logistics analyst. Write a highly analytical briefing (4-5 sentences) "
            f"explaining the supply chain disruption in this text. "
            f"This event triggered our {cats_str} risk monitors. "
            f"Crucially, explicitly evaluate the potential cascading impacts on dependent manufacturing sectors, specifically automotive and electronics. "
            f"Text: {clean_text[:3000]}"
        )
        response = gemini_model.call([{"role": "user", "content": prompt}])
        return response
    except Exception:
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
        for entry in feed.entries:
            raw_text = entry.title + " " + entry.get("summary", "")
            
            # 1. Gatekeeper: Only process if it matches the professor's matrix
            triggered_risks = check_risk_triggers(raw_text)
            
            if triggered_risks:
                print(f"Risk Detected ({triggered_risks[0]}): {entry.title[:30]}...")
                link = entry.link
                thumbnail = extract_thumbnail(link)
                
                # 2. AI Sector Impact Analysis
                summary = summarize_article(raw_text, triggered_risks)
                
                collected_articles.append({
                    "title": entry.title,
                    "link": link,
                    "thumbnail": thumbnail,
                    "summary": summary,
                    "risk_tags": triggered_risks,
                    "source": feed.feed.title if hasattr(feed.feed, 'title') else "Industry Intelligence",
                    "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                
                time.sleep(4) 
            else:
                print(f"Skipped (No Risk Triggers): {entry.title[:30]}...")
            
    os.makedirs("data", exist_ok=True)
    json_path = "data/intelligence.json"
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                existing_data = json.load(f)
            collected_articles = collected_articles + existing_data
        except json.JSONDecodeError:
            pass
            
    with open(json_path, "w") as f:
        json.dump(collected_articles, f, indent=4)
        
    print("Targeted risk intelligence gathered and saved.")

if __name__ == "__main__":
    gather_and_store()
