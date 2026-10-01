import os
import json
import time
import feedparser
from datetime import datetime, timedelta
from crewai import LLM
import wargame_engine  

# Configured with the active Google production endpoint
gemini_model = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def is_published_in_window(entry, days=8):
    parsed_time = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
    if parsed_time:
        try:
            entry_dt = datetime.fromtimestamp(time.mktime(parsed_time))
            return entry_dt >= datetime.now() - timedelta(days=days)
        except Exception:
            return True  
    return True

def is_relevant_article(entry):
    target_keywords = [
        "disruption", "shortage", "delay", "tariff", "strike", "climate", 
        "weather", "geopolitics", "risk", "labor", "capacity", "hurricane", 
        "war", "embargo", "cyberattack", "bottleneck",
        "packaged food", "fmcg", "food and beverage", "grocery", "cold chain", 
        "perishable", "rail", "railway", "freight train", "locomotive", 
        "road logistics", "trucking", "warehouse", "automation", "iot",
        "resilience", "mitigation", "single source", "regulatory",
        "artificial intelligence", "machine learning", "digital maturity", 
        "visibility", "maritime", "ports", "containerization", "strategic sourcing"
    ]
    content_block = f"{entry.title} {entry.get('summary', '')}".lower()
    return any(keyword in content_block for keyword in target_keywords)

def synthesize_with_retry(prompt, max_retries=5, initial_delay=10):
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            response = gemini_model.call([{"role": "user", "content": prompt}])
            if response and "Error generating synthesis" not in str(response) and "503" not in str(response):
                return response
            raise Exception(str(response))
        except Exception as e:
            print(f"Attempt {attempt} failed with error: {str(e)}")
            if attempt == max_retries:
                # Returns a strict ERROR flag instead of a string if it totally fails
                return "CRITICAL_FAILURE"
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2

def synthesize_weekly_report(raw_batch_text):
    prompt = f"""
    You are a Master-level Global Supply Chain Analyst. I am providing you with the complete batch of highly relevant global logistics news published this week. 
    Synthesize this complete dataset into a comprehensive 'Weekly Supply Chain Disruption Report'.
    
    Ensure ALL relevant developments are accounted for across the entire batch. Categorize the intelligence strictly into these five categories, focusing heavily on cascading impacts to RAILWAY INFRASTRUCTURE, PACKAGED FOODS (FMCG), COLD CHAIN LOGISTICS, WAREHOUSE AUTOMATION, and MARITIME PORTS:
    
    1. Geopolitics & Trade Policy
    2. Natural Disasters & Climate
    3. Logistics & Infrastructure
    4. Labor & Economic Factors
    5. Public Health & Safety
    
    CRITICAL CITATION RULE: To maintain absolute academic authenticity, EVERY SINGLE bullet point, factual statement, or analytical claim MUST end with an explicit source citation in parentheses at the very end of the line, detailing the publication and date based on the provided source (e.g., (FreightWaves, October 2026)).
    
    Format the output cleanly using professional Markdown headings, bolding, and bullet points. If there is no news for a specific category, state "No significant disruptions reported this week."
    
    Complete Raw News Batch:
    {raw_batch_text}
    """
    return synthesize_with_retry(prompt)

def gather_and_synthesize():
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
        
        source_name = feed.feed.get("title", "Industry Intelligence")
        
        for entry in feed.entries:
            if is_published_in_window(entry, days=8) and is_relevant_article(entry):
                summary = entry.get("summary") or entry.get("description") or ""
                pub_date = entry.get("published", "Recent")
                
                master_text_batch += f"Source: {source_name}\nTitle: {entry.title}\nPublished: {pub_date}\nSummary: {summary}\n\n"
                total_articles += 1
                
    print(f"Total relevant articles captured for this cycle: {total_articles}")
    
    if not master_text_batch.strip():
        print("No relevant articles identified within the current cycle window.")
        return

    print("Transmitting article batch to Gemini for Master Synthesis...")
    weekly_report_md = synthesize_weekly_report(master_text_batch)
    
    print("Transmitting identical batch to Gemini for War Game Generation...")
    wargame_report_md = wargame_engine.generate_wargame_scenario(master_text_batch)
    
    # --- THE NEW ERROR GATEKEEPER ---
    if weekly_report_md == "CRITICAL_FAILURE" or wargame_report_md == "CRITICAL_FAILURE":
        print("CRITICAL ERROR: Gemini API overloaded. Aborting save to protect database integrity.")
        raise SystemExit("Pipeline aborted due to upstream AI generation failure.")
    
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
        "master_report": weekly_report_md,
        "wargame_scenario": wargame_report_md 
    }
    
    existing_data.insert(0, new_report)
            
    with open(json_path, "w") as f:
        json.dump(existing_data, f, indent=4)
        
    print("Weekly Master Synthesis & War Game Scenario archived successfully.")

if __name__ == "__main__":
    gather_and_synthesize()
