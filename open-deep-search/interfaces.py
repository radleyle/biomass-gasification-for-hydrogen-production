from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SearchResult:
    title: str
    link: str
    snippet: str
    date: Optional[str] = None
    content: Optional[str] = None

@dataclass
class ResearchStep:
    query: str
    results: List[SearchResult]
    synthesis: str