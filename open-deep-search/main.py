import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from web_research_agent import WebResearchAgent

# Load environment variables
load_dotenv('.env.local')

async def main():
    agent = WebResearchAgent()

    # Read the topic from command line
    if len(sys.argv) < 2:
        print("Please provide a search topic to research")
        return
    
    topic = sys.argv[1]
    print(f"Starting research on: {topic}")

    max_research_steps = int(os.getenv('MAX_RESEARCH_STEPS', 5))
    
    # Perform multi-turn research
    research_steps = await agent.research_topic(topic, max_research_steps)
    
    # Generate final paper
    paper = await agent.generate_report(research_steps)
    
    print("Saving the report to file")
    
    # Save the paper to a file in research folder
    research_dir = Path('./research')
    research_dir.mkdir(exist_ok=True)
    
    filename = topic.replace(' ', '_').strip() + '.md'
    file_path = research_dir / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(paper)
    
    print("Research:")
    print(paper)

if __name__ == "__main__":
    asyncio.run(main())