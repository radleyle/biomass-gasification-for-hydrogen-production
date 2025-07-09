import os
import json
import asyncio
import aiohttp
from typing import List, Dict
from openai import AsyncOpenAI
from firecrawl import FirecrawlApp
from interfaces import SearchResult, ResearchStep
from prompts import (
    report_type_prompts,
    SYNTHESIS_PROMPT,
    FOLLOW_UP_QUERIES_PROMPT,
    REPORT_FORMATTING_REQUIREMENTS,
    RESEARCH_ASSISTANT_SYSTEM_PROMPT,
    RESEARCH_PAPER_WRITER_SYSTEM_PROMPT,
    QUERY_GENERATOR_SYSTEM_PROMPT
)

class WebResearchAgent:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        search_api_key = os.getenv('RAPIDAPI_KEY')
        firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
        ai_model = os.getenv('AI_MODEL')

        if not api_key:
            raise ValueError('OPENAI_API_KEY environment variable is not set')
        if not search_api_key:
            raise ValueError('RAPIDAPI_KEY environment variable is not set')
        if not firecrawl_api_key:
            raise ValueError('FIRECRAWL_API_KEY environment variable is not set')

        self.openai = AsyncOpenAI(api_key=api_key)
        self.search_api_key = search_api_key
        self.search_api_host = 'affordable-google-search-api.p.rapidapi.com'
        self.firecrawl = FirecrawlApp(api_key=firecrawl_api_key)
        self.model = ai_model or "gpt-4o"

    async def crawl_web_content(self, urls: List[str]) -> Dict[str, str]:
        print(f"🔍 Crawling {len(urls)} URLs for content...")
        content_map = {}

        for url in urls:
            try:
                print(f"  Crawling: {url}")
                scrape_result = self.firecrawl.scrape_url(url, params={'formats': ['markdown']})
                if not scrape_result.get('markdown'):
                    print(f"  ❌ No content found for {url}")
                    continue
                content_map[url] = scrape_result['markdown']
                print(f"  ✅ Successfully crawled {url}")
            except Exception as error:
                print(f"  ❌ Error crawling {url}: {error}")

        return content_map

    async def search_web(self, query: str) -> List[SearchResult]:
        print(f"🔎 Searching web for: \"{query}\"")
        try:
            url = f'https://{self.search_api_host}/api/google/search'
            headers = {
                'x-rapidapi-key': self.search_api_key,
                'x-rapidapi-host': self.search_api_host,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'query': query,
                'country': os.getenv('SEARCH_COUNTRY', 'us'),
                'lang': os.getenv('SEARCH_LANG', 'en'),
                'dateRange': os.getenv('SEARCH_DATE_RANGE', 'lastYear'),
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers=headers) as response:
                    result = await response.json()

            print(f"✅ Found {len(result['serp'])} search results")
            
            return [
                SearchResult(
                    title=item['title'],
                    link=item['link'],
                    snippet=item['snippet'],
                    date=item.get('date')
                )
                for item in result['serp'][:3]  # Take only first 3 results
            ]
        except Exception as error:
            print(f'❌ Search API error: {error}')
            return []

    def truncate_content(self, content: str, max_length: int = 2000) -> str:
        if len(content) <= max_length:
            return content
        return content[:max_length] + '... [truncated]'

    async def synthesize_results(
        self,
        topic: str,
        results: List[SearchResult],
        previous_findings: str
    ) -> str:
        print(f"🤔 Synthesizing {len(results)} search results...")

        # Crawl content from search result URLs
        urls = [r.link for r in results]
        page_contents = await self.crawl_web_content(urls)

        print('💭 Analyzing content with AI...')
        
        content_sections = []
        for result in results:
            content = page_contents.get(result.link, 'Content unavailable')
            truncated_content = self.truncate_content(content, 2000)
            content_sections.append(f"Content: {truncated_content}\n---")
        
        prompt = f"""
            Topic: {topic}
            Previous findings: {self.truncate_content(previous_findings, 1000)}
            
            New search results:
            {chr(10).join(content_sections)}
            
            {SYNTHESIS_PROMPT}
        """

        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": RESEARCH_ASSISTANT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        print('✅ Synthesis complete')
        return completion.choices[0].message.content or ''

    async def generate_follow_up_queries(
        self,
        topic: str,
        current_findings: str,
        previous_queries: List[str] = None
    ) -> List[str]:
        if previous_queries is None:
            previous_queries = []
            
        print('🔄 Generating follow-up queries...')
        
        prompt = f"""
            Based on our research about "{topic}" and our current findings:
            {self.truncate_content(current_findings, 800)}
            
            Previous queries already used: {', '.join(previous_queries)}
            
            Generate 3 NEW, DIFFERENT search queries that explore unexplored aspects of this topic.
            Avoid repeating or closely paraphrasing previous queries.
            
            {FOLLOW_UP_QUERIES_PROMPT}
        """

        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": QUERY_GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            function_call={"name": "get_search_queries"},
            functions=[
                {
                    "name": "get_search_queries",
                    "description": "Get three follow-up search queries",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "queries": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "A search query containing only alphanumeric characters, spaces, and basic punctuation"
                                },
                                "minItems": 3,
                                "maxItems": 3
                            }
                        },
                        "required": ["queries"]
                    }
                }
            ],
            temperature=0.7
        )

        response_content = completion.choices[0].message.function_call.arguments if completion.choices[0].message.function_call else None
        if not response_content:
            print('⚠️ No queries generated, using fallback')
            return [f"{topic} latest research"]

        try:
            queries_data = json.loads(response_content)
            queries = queries_data['queries']
            print(f"✅ Generated {len(queries)} follow-up queries")
            # Sanitize queries to ensure they're search-safe
            return [query.strip() for query in queries if query.strip()]
        except Exception as error:
            print(f'❌ Error parsing queries: {error}')
            return [f"{topic} latest research"]

    async def research_topic(self, topic: str, max_steps: int = 3) -> List[ResearchStep]:
        print(f"\n🚀 Starting research on: \"{topic}\" ({max_steps} steps)")
        steps = []
        current_query = topic
        all_findings = ''
        used_queries = [topic]

        for i in range(max_steps):
            print(f"\n📚 Research Step {i + 1}/{max_steps}")
            print(f"Current query: \"{current_query}\"")

            # Perform search
            results = await self.search_web(current_query)

            # Synthesize findings
            synthesis = await self.synthesize_results(topic, results, all_findings)
            all_findings += '\n' + synthesis

            # Store this research step
            steps.append(ResearchStep(
                query=current_query,
                results=results,
                synthesis=synthesis
            ))

            # Generate follow-up queries
            if i < max_steps - 1:
                follow_up_queries = await self.generate_follow_up_queries(topic, all_findings, used_queries)
                if follow_up_queries:
                    current_query = follow_up_queries[0]  # Use the first suggested query
                    used_queries.append(current_query)

        print('\n✅ Research complete!')
        return steps

    async def generate_report(self, steps: List[ResearchStep], report_type: str = 'comprehensive') -> str:
        print('\n📝 Generating report...')

        # Create a list of all unique sources
        sources = set()
        for step in steps:
            for result in step.results:
                sources.add(result.link)

        research_summary = '\n\n'.join([
            f"""
            Query: {step.query}
            Sources: {', '.join([r.link for r in step.results])}
            Findings: {self.truncate_content(step.synthesis, 1500)}
            """
            for step in steps
        ])

        sources_list = '\n'.join([f"[{i+1}] {url}" for i, url in enumerate(sources)])

        prompt = f"""
            Based on the following research:
            {self.truncate_content(research_summary, 8000)}
            
            {report_type_prompts.get(report_type, report_type_prompts['comprehensive'])}
            
            {REPORT_FORMATTING_REQUIREMENTS}
            
            Additional requirements:
            - When presenting numerical data, trends, or relationships, use Mermaid charts
            - Convert any tables with trends or relationships into visual charts
            - Each chart must have a clear title and description
            
            Available sources:
            {sources_list}
        """

        completion = await self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": RESEARCH_PAPER_WRITER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        paper = completion.choices[0].message.content or ''
        return paper