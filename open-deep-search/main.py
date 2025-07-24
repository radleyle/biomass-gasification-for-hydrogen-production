import os
import sys
import argparse
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from web_research_agent import WebResearchAgent
import re

# Load environment variables
# Try multiple paths for .env file
env_paths = ['../.env', '.env', '../.env.local']
env_loaded = False

for env_path in env_paths:
    if os.path.exists(env_path):
        print(f"Found .env file at: {env_path}")
        load_dotenv(env_path)
        env_loaded = True
        break

if not env_loaded:
    print("Warning: No .env file found. Trying to load from system environment...")
    load_dotenv()  # This will try to load from system environment

# Debug: Check if OPENAI_API_KEY is loaded
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"✅ OPENAI_API_KEY loaded (starts with: {api_key[:10]}...)")
else:
    print("❌ OPENAI_API_KEY not found in environment")

async def main():
    # Simplified argument parsing: only topic and max-steps
    parser = argparse.ArgumentParser(description='Web Research Agent for Biomass Gasification (Open Access Only)')
    parser.add_argument('topic', help='Search topic to research')
    parser.add_argument('--max-steps', type=int, default=5, help='Maximum research steps')
    args = parser.parse_args()

    agent = WebResearchAgent()
    topic = args.topic
    print(f"Starting open access research on: {topic}")
    max_research_steps = args.max_steps

    # Perform multi-turn research
    research_steps = await agent.research_topic(topic, max_research_steps)

    # Generate final paper
    paper = await agent.generate_report(research_steps, report_type='comprehensive')

    print("Saving the report to file")

    # Save the paper to a file in research folder
    research_dir = Path('./deep_search_results')
    research_dir.mkdir(exist_ok=True)

    # Filename does not depend on mode anymore
    # Extract gasification technology and yield type for filename
    topic_lower = topic.lower()
    # List of possible gasification technologies
    techs = [
        'steam gasification',
        'supercritical water gasification',
        'plasma gasification',
        'co2 gasification'
    ]
    yields = [
        'hydrogen yield',
        'carbon monoxide yield',
        'co yield'
    ]
    tech_match = next((t for t in techs if t in topic_lower), 'other')
    yield_match = next((y for y in yields if y in topic_lower), 'other')
    # Remove tech and yield from topic for the rest
    rest = topic_lower
    rest = re.sub(re.escape(tech_match), '', rest)
    rest = re.sub(re.escape(yield_match), '', rest)
    rest = rest.strip().replace(' ', '_').replace('/', '_').replace('\\', '_')
    # Build filename
    filename = f"{tech_match.replace(' ', '_')}_{yield_match.replace(' ', '_')}_{rest}.md"
    file_path = research_dir / filename

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(paper)

    print("Research:")
    print(paper)

if __name__ == "__main__":
    asyncio.run(main())