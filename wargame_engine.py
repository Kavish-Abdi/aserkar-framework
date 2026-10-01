import os
import time
from crewai import LLM

# Configured with the active Google production endpoint
gemini_model = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

def generate_wargame_scenario(scenario_text):
    prompt = f"""
    You are the analytical engine for the A.S.E.R.K.A.R. Framework. Your directive is to ingest global logistics, geopolitical, or financial news and autonomously generate a "War Game Scenario" predictive report.
    
    You must not wait for sequential prompts. Upon receiving the news text, automatically process the data and output the final response strictly as a single Markdown table.
    
    CRITICAL CITATION RULE:
    To maintain absolute academic authenticity, EVERY SINGLE bullet point, factual statement, or analytical claim within the table MUST end with an explicit source citation in parentheses at the very end of the line.
    The citation MUST strictly include:
    1. The publication/source name
    2. The exact article title in quotation marks
    3. The publication date
    
    Required Citation Format:
    ([Publication Name], "[Exact Article Title]", [Month Year])
    Example: (The Loadstar, "Red Sea Diversions Squeeze Global Container Capacity", September 2026)
    
    Do not leave any line uncited.
    
    Format the table exactly with the following four columns, focusing strictly on an industry-wide perspective (do not analyze country-wise):
    
    | Affected Industries | Duration Impact (1, 3, 6 Months) | Global Supply Chain Impact | Mitigation Strategies |
    | :--- | :--- | :--- | :--- |
    
    Column Definitions:
    1. Affected Industries: Identify the specific global industries directly or indirectly impacted by the ingested scenario.
    2. Duration Impact (1, 3, 6 Months): Detail the projected operational and financial impacts if the conflict or disruption continues for 1 month, 3 months, and 6 months.
    3. Global Supply Chain Impact: Detail the direct effects on the specific industry's global supply chain. You must include anticipated shifts in sourcing, alternate transit routes, or logistical bottlenecks (e.g., re-routing from the Strait of Hormuz to the Red Sea).
    4. Mitigation Strategies: Provide actionable, industry-specific mitigation and resilience strategies for the identified risks.
    
    Ingested News / Scenario Text:
    {scenario_text}
    """
    
    try:
        response = gemini_model.call([{"role": "user", "content": prompt}])
        return response
    except Exception as e:
        return f"Error generating War Game Scenario: {str(e)}"
