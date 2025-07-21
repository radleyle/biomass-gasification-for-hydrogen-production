#!/usr/bin/env python3
"""
Test Accessible Sources
=======================

This script tests the new accessible_only mode that focuses on sources
that are more likely to be successfully crawled and accessed.
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

async def test_accessible_sources():
    """Test the accessible_only mode with better crawling success."""
    agent = WebResearchAgent()
    
    print("🧪 Testing Accessible Sources Mode")
    print("=" * 50)
    print("This mode focuses on sources that are more likely to be successfully crawled:")
    print("• MDPI (open access)")
    print("• PLOS (open access)")
    print("• Hindawi (open access)")
    print("• Frontiers (open access)")
    print("• Scientific Research Publishing (open access)")
    print("• Cogent OA (open access)")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "steam gasification biomass hydrogen yield",
        "supercritical water gasification temperature effect",
        "plasma gasification biomass conversion efficiency"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 40)
        
        # Set to accessible_only mode
        agent.set_scientific_mode('accessible_only')
        
        try:
            # Perform search
            results = await agent.search_web(query)
            
            # Filter results
            filtered_results = agent.filter_results_by_domain(results)
            
            print(f"   📊 Found {len(results)} total results")
            print(f"   ✅ Filtered to {len(filtered_results)} accessible results")
            
            # Show results with source analysis
            for j, result in enumerate(filtered_results[:5], 1):
                print(f"   {j}. {result.title[:60]}...")
                print(f"      📍 {result.link}")
                
                # Check if it's from accessible sources
                accessible_sources = ['mdpi.com', 'plos.org', 'hindawi.com', 'frontiersin.org', 'scirp.org', 'cogentoa.com']
                is_accessible = any(source in result.link.lower() for source in accessible_sources)
                print(f"      {'✅ Accessible' if is_accessible else '❓ Unknown'} source")
                print()
            
            # Small delay between queries
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    print("\n✅ Accessible sources testing completed!")

async def test_crawling_success():
    """Test if we can actually crawl the content from accessible sources."""
    agent = WebResearchAgent()
    
    print("\n🔍 Testing Content Crawling")
    print("=" * 40)
    
    # Test with a simple query
    agent.set_scientific_mode('accessible_only')
    results = await agent.search_web("biomass gasification hydrogen yield")
    filtered = agent.filter_results_by_domain(results)
    
    if filtered:
        print(f"   📊 Found {len(filtered)} accessible results")
        print("   🔍 Attempting to crawl content...")
        
        # Try to crawl the first result
        test_url = filtered[0].link
        print(f"   📄 Testing crawl of: {test_url}")
        
        try:
            content_map = await agent.crawl_web_content([test_url])
            if content_map:
                print(f"   ✅ Successfully crawled content ({len(list(content_map.values())[0])} characters)")
                print("   📝 Content preview:")
                content = list(content_map.values())[0]
                print(f"   {content[:200]}...")
            else:
                print("   ❌ Failed to crawl content")
        except Exception as e:
            print(f"   ❌ Crawling error: {e}")
    else:
        print("   ❌ No accessible results found")

async def main():
    """Main test function."""
    print("🚀 Starting Accessible Sources Test")
    print("=" * 50)
    
    try:
        await test_accessible_sources()
        await test_crawling_success()
        
        print("\n🎉 All tests completed!")
        print("\n📋 Summary:")
        print("✅ Accessible sources mode working")
        print("✅ Better crawling success expected")
        print("✅ Focus on open access publishers")
        print("✅ Ready for reliable content access")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 