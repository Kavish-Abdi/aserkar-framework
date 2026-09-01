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

# The Professor's Complete Disruption Matrix
RISK_MATRIX = """
1. Geopolitics & Trade Policy: Tariffs, export controls, quotas, sanctions, embargoes, trade restrictions, customs delays, protectionism. Conflict & Security: War, military operations, blockades, piracy (e.g., Red Sea), terrorism, border closures. Political Instability: Protests, riots, coups, government shutdowns, civil unrest.
2. Natural Disasters & Climate: Extreme Weather (Typhoons, hurricanes, cyclones, blizzards, heatwaves, deep freezes), Geological (Earthquakes, tsunamis, volcanic eruptions, floods, landslides), Environmental Shifts (Droughts, wildfires, water scarcity).
3. Logistics & Infrastructure: Transportation Bottlenecks (Port congestion, route closures, canal blockages, airspace restrictions, rail derailments, trucking shortages), System Failures (Cyberattacks, ransomware, IT outages, power grid blackouts), Capacity Constraints (Container shortages, vessel delays, blank sailings, warehousing limits).
4. Labor & Economic Factors: Workforce Disruptions (Labor strikes, union disputes, worker shortages, walkouts, lockouts), Financial Instability (Supplier bankruptcies, hyperinflation, currency devaluation, raw material price spikes, liquidity crises).
5. Public Health & Safety: Health Crises (Pandemics, epidemics, disease outbreaks, quarantines, lockdowns), Industrial Accidents (Factory fires, chemical spills, hazardous leaks, component recalls).
"""

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

def analyze_article(text):
    clean_text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    
    prompt = f"""
    You are an elite logistics intelligence AI. Analyze this article against the following risk matrix:
    {RISK_MATRIX}
    
    Task:
    1. Write a 4-5 sentence executive briefing summarizing the disruption.
    2. Explicitly evaluate the potential cascading impacts on dependent manufacturing sectors, specifically automotive and electronics.
    3. At the very end of your response, add a new line starting exactly with "TAGS:" followed by a comma-separated list of the primary risk categories triggered (e.g., Geopolitics & Trade Policy, Logistics & Infrastructure). If no specific risks apply, output "TAGS: General Intelligence".
    
    Article Text: {clean_text[:3500]}
    """
    
    try:
        response = gemini_model.call([{"role": "user", "content": prompt}])
        
        # Parse the AI response to separate the summary from the risk tags
        lines = response.strip().split('\n')
        tags = ["General Intelligence"]
        summary_lines = []
        
        for line in lines:
            if line.strip().startswith("TAGS:"):
                tag_str = line.replace("TAGS:", "").strip()
                tags = [t.strip() for t in tag_str.split(",") if t.strip()]
            else:
                summary_lines.append(line)
                
        return "\n".join(summary_lines).strip(), tags
        
    except Exception:
        return clean_text[:350] + "...", ["General Intelligence"]

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
        # Process every article to cast a wide net
        for entry in feed.entries[:10]: 
            raw_text = entry.title + " " + entry.get("summary", "")
            
            print(f"Analyzing: {entry.title[:50]}...")
            link = entry.link
            thumbnail = extract_thumbnail(link)
            
            # The AI now acts as the filter and tagger
            summary, risk_tags = analyze_article(raw_text)
            
            collected_articles.append({
                "title": entry.title,
                "link": link,
                "thumbnail": thumbnail,
                "summary": summary,
                "risk_tags": risk_tags,
                "source": feed.feed.title if hasattr(feed.feed, 'title') else "Industry Intelligence",
                "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # 5-second sleep to prevent hitting Gemini API free-tier rate limits
            time.sleep(5) 
            
    os.makedirs("data", exist_ok=True)
    json_path = "data/intelligence.json"
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                existing_data = json.load(f)
            
            # Prevent duplicate articles based on the URL
            existing_urls = {item['link'] for item in existing_data}
            new_articles = [item for item in collected_articles if item['link'] not in existing_urls]
            
            collected_articles = new_articles + existing_data
        except json.JSONDecodeError:
            pass
            
    # Keep the latest 100 articles to prevent the dashboard from slowing down
    collected_articles = collected_articles[:100]
            
    with open(json_path, "w") as f:
        json.dump(collected_articles, f, indent=4)
        
    print("Intelligence gathered and saved.")

if __name__ == "__main__":
    gather_and_store()
