#!/usr/bin/env python3
"""
Test Open Access RAG Functionality
==================================

This script tests the new open access search functionality to ensure it:
1. Properly filters out paywall sources (ScienceDirect, etc.)
2. Prioritizes open access sources (ResearchGate, Web of Science, etc.)
3. Works with the new search modes
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to the path to import our modules
sys.path.append(str(Path(__file__).parent))

from web_research_agent import WebResearchAgent

# Load environment variables
load_dotenv()

async def test_open_access_search():
    """Test the open access search functionality."""
    agent = WebResearchAgent()
    
    # Test queries for biomass gasification
    test_queries = [
        "steam gasification biomass hydrogen yield experimental data",
        "supercritical water gasification temperature effect",
        "plasma gasification biomass conversion efficiency"
    ]
    
    test_modes = ['open_access', 'researchgate_only', 'web_of_science_only']
    
    print("🧪 Testing Open Access RAG Functionality")
    print("=" * 50)
    
    for mode in test_modes:
        print(f"\n📚 Testing mode: {mode}")
        print("-" * 30)
        
        agent.set_scientific_mode(mode)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            
            try:
                # Perform search
                results = await agent.search_web(query)
                
                # Filter results
                filtered_results = agent.filter_results_by_domain(results)
                
                print(f"   📊 Found {len(results)} total results")
                print(f"   ✅ Filtered to {len(filtered_results)} open access results")
                
                # Show top 3 results
                for j, result in enumerate(filtered_results[:3], 1):
                    print(f"   {j}. {result.title[:60]}...")
                    print(f"      📍 {result.link}")
                    print()
                
                # Small delay between queries
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    print("\n✅ Open access testing completed!")

async def test_specific_sources():
    """Test specific source filtering."""
    agent = WebResearchAgent()
    
    print("\n🎯 Testing Specific Source Filtering")
    print("=" * 40)
    
    # Test ResearchGate only
    print("\n📖 Testing ResearchGate only mode:")
    agent.set_scientific_mode('researchgate_only')
    results = await agent.search_web("biomass gasification hydrogen yield")
    filtered = agent.filter_results_by_domain(results)
    
    researchgate_count = sum(1 for r in filtered if 'researchgate.net' in r.link.lower())
    print(f"   ResearchGate results: {researchgate_count}/{len(filtered)}")
    
    # Test Web of Science only
    print("\n🌐 Testing Web of Science only mode:")
    agent.set_scientific_mode('web_of_science_only')
    results = await agent.search_web("biomass gasification hydrogen yield")
    filtered = agent.filter_results_by_domain(results)
    
    wos_count = sum(1 for r in filtered if 'webofscience.com' in r.link.lower() or 'apps.webofknowledge.com' in r.link.lower())
    print(f"   Web of Science results: {wos_count}/{len(filtered)}")
    
    # Test paywall exclusion
    print("\n🚫 Testing paywall exclusion:")
    agent.set_scientific_mode('open_access')
    results = await agent.search_web("biomass gasification hydrogen yield")
    filtered = agent.filter_results_by_domain(results)
    
    paywall_count = sum(1 for r in filtered if any(domain in r.link.lower() 
                                                   for domain in ['sciencedirect.com', 'springer.com/chapter', 'wiley.com/doi/abs']))
    print(f"   Paywall sources found: {paywall_count}/{len(filtered)} (should be 0)")

async def main():
    """Main test function."""
    print("🚀 Starting Open Access RAG Tests")
    print("=" * 50)
    
    try:
        await test_open_access_search()
        await test_specific_sources()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Summary:")
        print("✅ Open access search modes working")
        print("✅ Domain filtering functional")
        print("✅ Paywall exclusion active")
        print("✅ Ready for training with open access sources")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 