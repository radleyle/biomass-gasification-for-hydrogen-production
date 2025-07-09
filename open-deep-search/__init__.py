# research_feature/__init__.py
"""
Open Deep Search - AI-powered web research tool
"""

from .web_research_agent import WebResearchAgent
from .interfaces import SearchResult, ResearchStep

__all__ = ['WebResearchAgent', 'SearchResult', 'ResearchStep']