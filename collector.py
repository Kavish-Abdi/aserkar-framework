import os
import json
import feedparser
from datetime import datetime
from crewai import LLM

# Configured with the current active Google production endpoint
gemini_model = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def synthesize_weekly_report(raw_batch_text):
    prompt = f"""
    You are a Master-level Global Supply Chain Analyst. I am providing you with a raw batch of this week's global logistics news. 
    Synthesize this data into a single comprehensive 'Weekly Supply Chain Disruption Report'.
    
    You MUST categorize the intelligence strictly into these five categories. Focus heavily on cascading impacts to the automotive and electronics manufacturing sectors:
    
    1. Geopolitics & Trade Policy (Tariffs, export controls, quotas, sanctions, embargoes, trade restrictions, customs delays, protectionism, war, military operations, blockades, piracy, terrorism, border closures, protests, riots, coups, government shutdowns, civil unrest)
    2. Natural Disasters & Climate (Extreme weather like typhoons, hurricanes, cyclones, blizzards, heatwaves, deep freezes; Geological events like earthquakes, tsunamis, volcanic eruptions, floods, landslides; Environmental shifts like droughts, wildfires, water scarcity affecting manufacturing)
    3. Logistics & Infrastructure (Transportation bottlenecks like port congestion, route closures, maritime canal blockages, airspace restrictions, rail derailments, trucking shortages; System failures like cyberattacks, ransomware, IT network outages, power grid blackouts; Capacity constraints like shipping container shortages, vessel delays, blank sailings, warehousing limits)
    4. Labor & Economic Factors (Workforce disruptions like labor strikes, union disputes, structural worker shortages, walkouts, lockouts; Financial instability like supplier bankruptcies, hyperinflation, extreme currency devaluation, raw material price spikes, liquidity crises)
    5. Public Health & Safety (Health crises like pandemics, epidemics, disease outbreaks, mandatory quarantines, factory lockdowns; Industrial accidents like factory fires, chemical spills, hazardous material leaks, component recalls)
    
    Format the output cleanly using professional Markdown headings, bolding, and bullet points. If there is no news for a specific category, state "No significant disruptions reported this week."
    
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
    
    # Reset old entries and save the structured master weekly report
    report_data = [{
        "date_collected": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "master_report": weekly_report_md
    }]
            
    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=4)
        
    print("Weekly Master Synthesis saved successfully.")

if __name__ == "__main__":
    gather_and_synthesize()
