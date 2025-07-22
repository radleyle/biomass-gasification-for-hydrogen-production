import asyncio
from gpt_researcher import GPTResearcher
from dotenv import load_dotenv
import os
from datetime import datetime
import sys
# Load environment variables from .env
load_dotenv()

async def run_web_research(query):
    researcher = GPTResearcher(
        query=query,
        report_source="web",  # Use "web" for web search only
        # You can add more config options here if needed
    )
    # Conduct research (scrapes and summarizes sources)
    context = await researcher.conduct_research()
    # Optionally, generate a report
    report = await researcher.write_report()
    return context, report

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter your research query: ")
    context, report = asyncio.run(run_web_research(query))
    print("First 500 chars of report:\n", report[:500])
    # For structured data, you can use the context variable
    # Example: print(context)
    
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c if c.isalnum() or c in " _-" else "_" for c in query)[:40]
    report_path = f"reports/{timestamp}_{safe_query}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nFull report saved to: {report_path}")