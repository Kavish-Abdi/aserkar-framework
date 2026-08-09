import os
import json
from datetime import datetime
from crewai import Agent, Task, Crew, Process

def fetch_local_intelligence():
    json_path = "data/intelligence.json"
    if not os.path.exists(json_path):
        return "No background intelligence gathered yet."
        
    with open(json_path, "r") as f:
        articles = json.load(f)
        
    formatted_data = "\n".join([f"- {item['title']}: {item['summary']}" for item in articles])
    return formatted_data

def run_aserkar_simulation():
    historical_data = fetch_local_intelligence()

    analyst = Agent(
        role="Intelligence Analyst",
        goal="Synthesize news into converging risk factors affecting the overall packaged foods sector and railway logistics.",
        backstory="Expert at tracking weak signals across regional railway networks and large-scale packaged food distribution channels.",
        verbose=True
    )

    red_team = Agent(
        role="Red Team Architect",
        goal="Design a 3-turn wargame scenario based on the analyst's risk factors.",
        backstory="Specialist in designing tabletop exercises that stress-test logistics networks and automated sensor integrations like StormNode.",
        verbose=True
    )

    analyze_task = Task(
        description=f"Analyze this aggregated intelligence payload: {historical_data}. Identify 3 compounding risk factors.",
        expected_output="A bulleted list of 3 specific, converging operational risks.",
        agent=analyst
    )

    wargame_task = Task(
        description="Create a 3-turn wargame scenario from the identified risks. Focus on the impact on the overall packaged foods sector.",
        expected_output="A structured tabletop exercise document with distinct turns and decision points.",
        agent=red_team
    )

    crew = Crew(
        agents=[analyst, red_team],
        tasks=[analyze_task, wargame_task],
        process=Process.sequential
    )

    result = crew.kickoff()
    
    # Save scenario output to markdown file
    os.makedirs("scenarios", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"scenarios/Aserkar_Wargame_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(str(result))
        
    return str(result)
