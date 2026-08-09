import os
from crewai import Agent, Task, Crew, Process, LLM

# ... (keep your fetch_local_intelligence function up here)

def run_aserkar_simulation():
    historical_data = fetch_local_intelligence()

    # 1. Define the separate LLMs
    gemini_model = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=os.environ.get("GEMINI_API_KEY")
    )
    
    openai_model = LLM(
        model="openai/gpt-4o-mini",
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # 2. Assign Gemini to the Analyst
    analyst = Agent(
        role="Intelligence Analyst",
        goal="Synthesize news into converging risk factors affecting the overall packaged foods sector and railway logistics.",
        backstory="Expert at tracking weak signals across regional railway networks and large-scale packaged food distribution channels.",
        verbose=True,
        llm=gemini_model
    )

    # 3. Assign OpenAI to the Red Team
    red_team = Agent(
        role="Red Team Architect",
        goal="Design a 3-turn wargame scenario based on the analyst's risk factors.",
        backstory="Specialist in designing tabletop exercises that stress-test logistics networks and automated sensor integrations like StormNode.",
        verbose=True,
        llm=openai_model
    )

    # ... (Keep the rest of your Tasks and Crew kickoff exactly the same)
