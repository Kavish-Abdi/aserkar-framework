import os
import json
import time
from crewai import LLM

gemini_model = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def generate_wargame_scenario(scenario_text, max_retries=15, initial_delay=20):
    prompt = f"""
    You are the analytical engine for the A.S.E.R.K.A.R. Framework. 
    Your directive is to ingest global logistics news and autonomously generate a "War Game Scenario" predictive report.
    
    CRITICAL OUTPUT FORMAT:
    You must output STRICTLY a valid JSON object. Do not include any markdown wrappers (like ```json), conversational text, or introductions. Just the raw JSON string.
    
    The JSON object MUST have exactly these four keys:
    1. "table": A markdown string of the 4-column War Game table. Do NOT put citations inline.
       Columns: | Affected Industries | Duration Impact (1, 3, 6 Months) | Global Supply Chain Impact | Mitigation Strategies |
    2. "references": A markdown string containing a numbered list of all sources used, acting as a Bibliography at the end of the report. (Format: 1. Publication Name, "Article Title", Date).
    3. "mermaid": A valid Mermaid.js flowchart string (starting with 'graph TD' or 'flowchart TD') visualizing the primary supply chain disruption and alternate mitigation routing.
    4. "coordinates": A list of JSON objects containing "lat" and "lon" float values representing the geographic locations of the primary disruptions (e.g., ports, straits, rail hubs).
    
    Ingested News:
    {scenario_text}
    """
    
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            print(f"War Game Engine: Attempt {attempt} of {max_retries}...")
            response = gemini_model.call([{"role": "user", "content": prompt}])
            
            if "503" in str(response):
                raise Exception("503 UNAVAILABLE - Server Overloaded")
            
            # Strip potential markdown formatting from the API response
            if response.startswith("```json"):
                response = response.replace("```json", "", 1)
            if response.endswith("```"):
                response = response[:-3]
                
            return json.loads(response.strip())
            
        except Exception as e:
            print(f"War Game Engine Attempt {attempt} failed: {str(e)}")
            if attempt == max_retries:
                return {"error": f"Error generating War Game Scenario after {max_retries} retries: {str(e)}"}
            time.sleep(delay)
            # Capping delay at 120 seconds max
            delay = min(delay * 2, 120)
