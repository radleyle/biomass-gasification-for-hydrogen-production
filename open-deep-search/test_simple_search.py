#!/usr/bin/env python3
"""
Simple Search Test
=================

This script tests the search functionality with less restrictive filtering
to ensure we get results for biomass gasification research.
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

async def test_simple_search():
    """Test search with less restrictive filtering."""
    agent = WebResearchAgent()
    
    # Test with general mode first
    print("🧪 Testing Simple Search")
    print("=" * 40)
    
    # Test 1: General search
    print("\n📚 Test 1: General search mode")
    agent.set_scientific_mode('general')
    results = await agent.search_web("steam gasification biomass hydrogen yield")
    print(f"   📊 Found {len(results)} results")
    
    # Test 2: Open access mode
    print("\n📚 Test 2: Open access mode")
    agent.set_scientific_mode('open_access')
    results = await agent.search_web("steam gasification biomass hydrogen yield")
    filtered = agent.filter_results_by_domain(results)
    print(f"   📊 Found {len(results)} total, {len(filtered)} filtered results")
    
    # Test 3: ResearchGate only
    print("\n📚 Test 3: ResearchGate only mode")
    agent.set_scientific_mode('researchgate_only')
    results = await agent.search_web("steam gasification biomass hydrogen yield")
    filtered = agent.filter_results_by_domain(results)
    print(f"   📊 Found {len(results)} total, {len(filtered)} filtered results")
    
    # Show some results
    if filtered:
        print("\n📋 Sample Results:")
        for i, result in enumerate(filtered[:3], 1):
            print(f"   {i}. {result.title[:60]}...")
            print(f"      📍 {result.link}")
            print()
    else:
        print("\n❌ No results found. Trying broader search...")
        
        # Try broader search
        agent.set_scientific_mode('general')
        results = await agent.search_web("biomass gasification hydrogen")
        print(f"   📊 Broader search found {len(results)} results")
        
        if results:
            print("\n📋 Broader Search Results:")
            for i, result in enumerate(results[:3], 1):
                print(f"   {i}. {result.title[:60]}...")
                print(f"      📍 {result.link}")
                print()

async def main():
    """Main test function."""
    print("🚀 Starting Simple Search Test")
    print("=" * 40)
    
    try:
        await test_simple_search()
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 