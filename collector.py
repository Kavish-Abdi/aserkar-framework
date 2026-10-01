import os
import json
import time
import feedparser
from datetime import datetime, timedelta
from crewai import LLM

# Configured with the active Google production endpoint
gemini_model = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def is_published_in_window(entry, days=8):
    """
    Checks if the entry was published within the target time window.
    An 8-day window ensures zero gaps between 7-day scheduled cron runs.
    """
    parsed_time = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if parsed_time:
        try:
            entry_dt = datetime.fromtimestamp(time.mktime(parsed_time))
            return entry_dt >= datetime.now() - timedelta(days=days)
        except Exception:
            return True  
    return True

def is_relevant_article(entry):
    """
    Acts as a first-pass gatekeeper. Only allows articles containing keywords related to 
    Prof. Aserkar's specific focus areas: FMCG, Railway, AI maturity, and Maritime risks.
    """
    target_keywords = [
        # Core Disruption Vectors
        "disruption", "shortage", "delay", "tariff", "strike", "climate", 
        "weather", "geopolitics", "risk", "labor", "capacity", "hurricane", 
        "war", "embargo", "cyberattack", "bottleneck",
        
        # Specific Industries (Rail, Food, Automation)
        "packaged food", "fmcg", "food and beverage", "grocery", "cold chain", 
        "perishable", "rail", "railway", "freight train", "locomotive", 
        "road logistics", "trucking", "warehouse", "automation", "iot",
        
        # Strategic & Tech Focus Areas
        "resilience", "mitigation", "single source", "regulatory",
        "artificial intelligence", "machine learning", "digital maturity", 
        "visibility", "maritime", "ports", "containerization", "strategic sourcing"
    ]
    
    content_block = f"{entry.title} {entry.get('summary', '')}".lower()
    return any(keyword in content_block for keyword in target_keywords)

def synthesize_with_retry(prompt, max_retries=3, initial_delay=5):
    """Attempt to call the Gemini model with exponential backoff to handle 503 Overloads."""
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            response = gemini_model.call([{"role": "user", "content": prompt}])
            if response and "Error generating synthesis" not in str(response):
                return response
            raise Exception(str(response))
        except Exception as e:
            print(f"Attempt {attempt} failed with error: {str(e)}")
            if attempt == max_retries:
                return f"Error generating synthesis after {max_retries} retries: {str(e)}"
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2

def synthesize_weekly_report(raw_batch_text):
    prompt = f"""
    You are a Master-level Global Supply Chain Analyst. I am providing you with the complete batch of highly relevant global logistics news published this week. 
    Synthesize this complete dataset into a comprehensive 'Weekly Supply Chain Disruption Report'.
    
    Ensure ALL relevant developments are accounted for across the entire batch. Categorize the intelligence strictly into these five categories, focusing heavily on cascading impacts to RAILWAY INFRASTRUCTURE, PACKAGED FOODS (FMCG), COLD CHAIN LOGISTICS, WAREHOUSE AUTOMATION, and MARITIME PORTS:
    
    1. Geopolitics & Trade Policy (Tariffs, export controls, quotas, sanctions, embargoes, trade restrictions, customs delays, protectionism, war, military operations, blockades, piracy, terrorism, border closures, protests, riots, coups, government shutdowns, civil unrest)
    2. Natural Disasters & Climate (Extreme weather like typhoons, hurricanes, cyclones, blizzards, heatwaves, deep freezes; Geological events like earthquakes, tsunamis, volcanic eruptions, floods, landslides; Environmental shifts like droughts, wildfires, water scarcity affecting manufacturing)
    3. Logistics & Infrastructure (Transportation bottlenecks like port congestion, route closures, maritime canal blockages, airspace restrictions, rail derailments, trucking shortages; System failures like cyberattacks, ransomware, IT network outages, power grid blackouts; Capacity constraints like shipping container shortages, vessel delays, blank sailings, warehousing limits)
    4. Labor & Economic Factors (Workforce disruptions like labor strikes, union disputes, structural worker shortages, walkouts, lockouts; Financial instability like supplier bankruptcies, hyperinflation, extreme currency devaluation, raw material price spikes, liquidity crises)
    5. Public Health & Safety (Health crises like pandemics, epidemics, disease outbreaks, mandatory quarantines, factory lockdowns; Industrial accidents like factory fires, chemical spills, hazardous material leaks, component recalls)
    
    Format the output cleanly using professional Markdown headings, bolding, and bullet points. If there is no news for a specific category, state "No significant disruptions reported this week."
    
    Complete Raw News Batch:
    {raw_batch_text}
    """
    
    return synthesize_with_retry(prompt)

def gather_and_synthesize():
    # Expanded list of top-tier intelligence platforms
    rss_urls = [
        "https://www.supplychainbrain.com/rss",
        "https://feeds.feedburner.com/logisticsmgmt/latest",
        "https://procureinsights.com/feed/",
        "https://news.google.com/rss/search?q=wall+street+journal+supply+chain+logistics",
        "https://www.freightwaves.com/feed",
        "https://theloadstar.com/feed/",
        "https://www.supplychaindive.com/feeds/news/",
        "https://www.railwayage.com/feed/",
        "https://www.railfreight.com/feed/",
        "https://railway-news.com/feed/"
    ]
    
    print("Gathering complete macro intelligence batch...")
    master_text_batch = ""
    total_articles = 0
    
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        for entry in feed.entries:
            if is_published_in_window(entry, days=8) and is_relevant_article(entry):
                summary = entry.get("summary") or entry.get("description") or ""
                pub_date = entry.get("published", "Recent")
                master_text_batch += f"Title: {entry.title}\nPublished: {pub_date}\nSummary: {summary}\n\n"
                total_articles += 1
                
    print(f"Total relevant articles captured for this cycle: {total_articles}")
    
    if not master_text_batch.strip():
        print("No relevant articles identified within the current cycle window.")
        return

    print("Transmitting entirely relevant article batch to Gemini for Master Synthesis...")
    weekly_report_md = synthesize_weekly_report(master_text_batch)
    
    os.makedirs("data", exist_ok=True)
    json_path = "data/intelligence.json"
    
    existing_data = []
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            pass
    
    new_report = {
        "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "articles_analyzed": total_articles,
        "master_report": weekly_report_md
    }
    
    existing_data.insert(0, new_report)
            
    with open(json_path, "w") as f:
        json.dump(existing_data, f, indent=4)
        
    print("Weekly Master Synthesis archived successfully.")

if __name__ == "__main__":
    gather_and_synthesize()
