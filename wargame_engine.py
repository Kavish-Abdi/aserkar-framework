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
    You are a Master-level Global Supply Chain Analyst and Strategic Wargaming Expert.
    Analyze the provided news or conflict scenario and generate a "War Game Scenario" report.
    
    CRITICAL INSTRUCTIONS:
    1. Output Format: Present the final output STRICTLY in a Markdown tabulated format. Do not write introductory or concluding paragraphs outside the table.
    2. Perspective: The analysis MUST be from an INDUSTRY-WIDE perspective (e.g., Automakers, FMCG, Rail Freight), NOT country-wise.
    3. Citations: You MUST append explicit source citations in parentheses (e.g., "(Wall Street Journal, August 2026)") next to the information derived from the provided news source.
    
    The table MUST contain exactly these four columns:
    
    | Affected Industries | Duration Impact | Global Supply Chain Impact | Mitigation Strategies |
    | :--- | :--- | :--- | :--- |
    
    Column Definitions:
    - Affected Industries: Which specific global industries are going to be affected by this conflict?
    - Duration Impact: Detail the projected impact scaling across three timeframes: 1 month, 3 months, and 6 months.
    - Global Supply Chain Impact: What is the direct impact on the global supply chain of that particular industry? (Explicitly include potential shifts in sourcing, modal shifts, or alternate routing, such as shifting from the Strait of Hormuz to the Red Sea, or ocean-to-rail shifts).
    - Mitigation Strategies: What are the recommended mitigating strategies and resilience tactics for each identified scenario?
    
    Scenario / Breaking News Text:
    {scenario_text}
    """
    
    try:
        response = gemini_model.call([{"role": "user", "content": prompt}])
        return response
    except Exception as e:
        return f"Error generating War Game Scenario: {str(e)}"
