#!/usr/bin/env python3
"""
Open Access RAG Training Script
===============================

This script trains the RAG model specifically on open access sources:
- Web of Science (free abstracts and some full texts)
- ResearchGate (free publications and preprints)
- arXiv (free preprints)
- PubMed (free abstracts and some full texts)

This avoids expensive paywall sources like ScienceDirect.
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add the current directory to the path to import our modules
sys.path.append(str(Path(__file__).parent))

from web_research_agent import WebResearchAgent
from interfaces import ResearchStep

# Load environment variables
load_dotenv()

class OpenAccessRAGTrainer:
    def __init__(self):
        self.agent = WebResearchAgent()
        self.training_data = []
        self.output_dir = Path("open_access_training_data")
        self.output_dir.mkdir(exist_ok=True)
        
    def get_training_queries(self) -> List[str]:
        """Define training queries for biomass gasification research."""
        return [
            # Steam gasification
            "steam gasification biomass hydrogen yield experimental data",
            "steam gasification temperature pressure effect hydrogen production",
            "steam gasification biomass feedstock comparison wood chips rice husk",
            "steam gasification catalyst effect hydrogen yield",
            "steam gasification reaction kinetics biomass",
            
            # Supercritical water gasification
            "supercritical water gasification biomass hydrogen yield",
            "supercritical water gasification temperature pressure optimization",
            "supercritical water gasification biomass types comparison",
            "supercritical water gasification reaction mechanism",
            "supercritical water gasification catalyst selection",
            
            # Plasma gasification
            "plasma gasification biomass hydrogen production",
            "plasma gasification temperature effect hydrogen yield",
            "plasma gasification biomass conversion efficiency",
            "plasma gasification reactor design optimization",
            "plasma gasification energy efficiency analysis",
            
            # CO2 gasification
            "CO2 gasification biomass hydrogen yield experimental",
            "CO2 gasification temperature pressure effect",
            "CO2 gasification biomass carbon monoxide production",
            "CO2 gasification reaction kinetics",
            "CO2 gasification catalyst performance",
            
            # Environmental impact
            "biomass gasification environmental impact LCA",
            "biomass gasification greenhouse gas emissions",
            "biomass gasification energy efficiency comparison",
            "biomass gasification waste management",
            "biomass gasification sustainability assessment",
            
            # Economic analysis
            "biomass gasification economic feasibility",
            "biomass gasification cost analysis hydrogen production",
            "biomass gasification commercialization challenges",
            "biomass gasification market potential",
            "biomass gasification investment requirements"
        ]
    
    async def train_on_query(self, query: str, mode: str = 'open_access') -> Dict[str, Any]:
        """Train the RAG model on a specific query using open access sources."""
        print(f"\n🔬 Training on query: {query}")
        print(f"📚 Using mode: {mode}")
        
        # Set the agent to open access mode
        self.agent.set_scientific_mode(mode)
        
        # Perform research
        steps = await self.agent.research_topic(query, max_steps=3)
        
        # Generate comprehensive report
        report = await self.agent.generate_report(steps, report_type='comprehensive')
        
        # Collect training data
        training_entry = {
            'query': query,
            'mode': mode,
            'timestamp': datetime.now().isoformat(),
            'steps': [
                {
                    'query': step.query,
                    'findings': step.findings,
                    'sources': [str(result) for result in step.results]
                }
                for step in steps
            ],
            'final_report': report,
            'total_sources': sum(len(step.results) for step in steps)
        }
        
        return training_entry
    
    async def train_full_dataset(self, modes: List[str] = None):
        """Train the RAG model on the full dataset using multiple modes."""
        if modes is None:
            modes = ['open_access', 'researchgate_only', 'web_of_science_only']
        
        queries = self.get_training_queries()
        
        print(f"🚀 Starting RAG training with {len(queries)} queries across {len(modes)} modes")
        print(f"📊 Total training iterations: {len(queries) * len(modes)}")
        
        all_training_data = []
        
        for mode in modes:
            print(f"\n📚 Training in {mode} mode...")
            mode_data = []
            
            for i, query in enumerate(queries, 1):
                print(f"\n--- Training {i}/{len(queries)} in {mode} mode ---")
                
                try:
                    training_entry = await self.train_on_query(query, mode)
                    mode_data.append(training_entry)
                    
                    # Save progress after each query
                    self.save_training_data(mode_data, mode)
                    
                    # Small delay to be respectful to APIs
                    await asyncio.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Error training on query '{query}' in {mode} mode: {e}")
                    continue
            
            all_training_data.extend(mode_data)
        
        # Save complete dataset
        self.save_training_data(all_training_data, 'complete_dataset')
        
        # Generate training summary
        self.generate_training_summary(all_training_data)
        
        return all_training_data
    
    def save_training_data(self, data: List[Dict], filename: str):
        """Save training data to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.output_dir / f"{filename}_{timestamp}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved training data to: {filepath}")
    
    def generate_training_summary(self, training_data: List[Dict]):
        """Generate a summary of the training results."""
        summary = {
            'total_queries': len(training_data),
            'modes_used': list(set(entry['mode'] for entry in training_data)),
            'total_sources': sum(entry['total_sources'] for entry in training_data),
            'average_sources_per_query': sum(entry['total_sources'] for entry in training_data) / len(training_data),
            'training_timestamp': datetime.now().isoformat(),
            'query_categories': {
                'steam_gasification': len([q for q in self.get_training_queries() if 'steam' in q.lower()]),
                'scw_gasification': len([q for q in self.get_training_queries() if 'supercritical' in q.lower()]),
                'plasma_gasification': len([q for q in self.get_training_queries() if 'plasma' in q.lower()]),
                'co2_gasification': len([q for q in self.get_training_queries() if 'co2' in q.lower()]),
                'environmental': len([q for q in self.get_training_queries() if 'environmental' in q.lower() or 'lca' in q.lower()]),
                'economic': len([q for q in self.get_training_queries() if 'economic' in q.lower() or 'cost' in q.lower()])
            }
        }
        
        summary_file = self.output_dir / f"training_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Training Summary:")
        print(f"   Total queries processed: {summary['total_queries']}")
        print(f"   Modes used: {', '.join(summary['modes_used'])}")
        print(f"   Total sources collected: {summary['total_sources']}")
        print(f"   Average sources per query: {summary['average_sources_per_query']:.1f}")
        print(f"   Summary saved to: {summary_file}")

async def main():
    """Main function to run the open access RAG training."""
    trainer = OpenAccessRAGTrainer()
    
    print("🎯 Open Access RAG Training for Biomass Gasification")
    print("=" * 60)
    print("This will train the RAG model using free, open access sources:")
    print("• Web of Science (free abstracts)")
    print("• ResearchGate (free publications)")
    print("• arXiv (free preprints)")
    print("• PubMed (free abstracts)")
    print("• Avoiding expensive paywall sources like ScienceDirect")
    print("=" * 60)
    
    # You can customize which modes to use
    modes = ['web_of_science_only']  # Focus on Web of Science (highest quality)
    
    try:
        training_data = await trainer.train_full_dataset(modes)
        print(f"\n✅ Training completed successfully!")
        print(f"📁 Training data saved in: {trainer.output_dir}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Training interrupted by user")
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 