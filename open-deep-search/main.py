import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from web_research_agent import WebResearchAgent

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
    research_dir = Path('./deep_search_results')
    research_dir.mkdir(exist_ok=True)
    
    filename = topic.replace(' ', '_').replace('/', '_').replace('\\', '_').strip() + '.md'
    file_path = research_dir / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(paper)
    
    print("Research:")
    print(paper)

if __name__ == "__main__":
    asyncio.run(main())