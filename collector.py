import os
import json
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from crewai import LLM

gemini_model = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def synthesize_weekly_report(raw_batch_text):
    prompt = f"""
    You are a Master-level Global Supply Chain Analyst. I am providing you with a raw batch of this week's global logistics news. 
    Synthesize this data into a single 'Weekly Supply Chain Disruption Report'.
    
    You MUST categorize the intelligence strictly into these five categories. Focus heavily on cascading impacts to the automotive and electronics sectors.
    
    1. Geopolitics & Trade Policy (Tariffs, export controls, quotas, sanctions, embargoes, war, piracy, blockades, unrest)
    2. Natural Disasters & Climate (Extreme weather, geological events, environmental shifts, droughts, water scarcity)
    3. Logistics & Infrastructure (Port congestion, route closures, airspace restrictions, cyberattacks, blank sailings, capacity limits)
    4. Labor & Economic Factors (Strikes, union disputes, bankruptcies, hyperinflation, raw material price spikes)
    5. Public Health & Safety (Pandemics, factory fires, chemical spills, hazardous leaks, recalls)
    
    Format the output as clean Markdown using bolding and bullet points. If there is no news for a specific category, write "No significant disruptions detected this week."
    
    Raw News Batch:
    {raw_batch_text[:35000]}
    """
    
    try:
        response = gemini_model.call([{"role": "user", "content": prompt}])
        return response
    except Exception as e:
        return f"Error generating synthesis: {str(e)}"

def gather_and_synthesize():
    rss_urls = [
        "https://www.supplychainbrain.com/rss",
        "https://feeds.feedburner.com/logisticsmgmt/latest",
        "https://procureinsights.com/feed/",
        "https://news.google.com/rss/search?q=wall+street+journal+supply+chain+logistics"
    ]
    
    print("Gathering macro intelligence batch...")
    master_text_batch = ""
    
    for rss in rss_urls:
        feed = feedparser.parse(rss)
        for entry in feed.entries[:15]: 
            master_text_batch += f"Title: {entry.title}\nSummary: {entry.get('summary', '')}\n\n"
            
    print("Transmitting to Gemini for Master Synthesis...")
    weekly_report_md = synthesize_weekly_report(master_text_batch)
    
    os.makedirs("data", exist_ok=True)
    json_path = "data/intelligence.json"
    
    # We are completely wiping the old individual cards and saving just the Master Report
    report_data = [{
        "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "master_report": weekly_report_md
    }]
            
    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print("Weekly Master Synthesis saved.")

if __name__ == "__main__":
    gather_and_synthesize()
