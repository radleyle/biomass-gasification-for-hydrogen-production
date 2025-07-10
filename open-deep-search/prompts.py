from typing import Dict

# Enhanced prompts for scientific biomass gasification research
scientific_research_prompts: Dict[str, str] = {
    "biomass_gasification": """
        Generate a scientific research report that prioritizes papers with:
        1. EXPERIMENTAL DATA with standardized units (mol/kg, mmol/g, g/kg biomass)
        2. COMPLETE METHODOLOGY sections including:
           - Specific feedstock type and source location
           - Detailed experimental conditions (temperature, pressure, time)
           - Reactor type and configuration
           - Gas analysis methods
        3. COMPREHENSIVE RESULTS with:
           - Hydrogen yield data in mol/kg or mmol/g
           - Carbon monoxide yield data in consistent units
           - Comparison with other feedstocks or conditions
        4. PEER-REVIEWED sources from established journals
        5. RECENT publications (2015-2024) with reproducible methodologies
        
        Focus on papers that provide both feedstock characterization AND experimental yields in the same study.
        Prioritize papers with tabulated data and clear experimental sections.
    """,
    "experimental_validation": """
        Generate a technical validation report focusing on:
        1. REPRODUCIBLE experimental protocols with clear methodologies
        2. STANDARDIZED REPORTING of yield data in consistent units
        3. FEEDSTOCK CHARACTERIZATION including proximate/ultimate analysis
        4. OPERATING CONDITION specifications (temperature ranges, residence times)
        5. QUALITY CONTROL measures and error analysis
        6. COMPARATIVE STUDIES across different feedstocks or technologies
        7. SCALED EXPERIMENTAL setups from lab to pilot scale
        
        Emphasize papers that allow direct comparison and data extraction for RAG systems.
    """,
    "unit_standardized": """
        Generate a data-focused report emphasizing:
        1. Papers reporting yields in MOL/KG or MMOL/G units specifically
        2. CONVERSION FACTORS and unit standardization methods
        3. FEEDSTOCK-SPECIFIC data with clear biomass identification
        4. TABULATED RESULTS that can be directly extracted
        5. MULTIPLE OPERATING CONDITIONS in the same study
        6. STATISTICAL ANALYSIS of experimental uncertainty
        7. BENCHMARK COMPARISONS with established technologies
        
        Prioritize sources with clear data tables and comprehensive experimental details.
    """
}

report_type_prompts: Dict[str, str] = {
    "comprehensive": """
        Generate a comprehensive report that:
        1. Provides an executive summary
        2. Outlines key findings and insights
        3. Presents detailed analysis with supporting evidence
        4. Includes relevant statistics and data
        5. Discusses market/industry implications
        6. Highlights best practices and recommendations
        7. Addresses challenges and limitations
        8. Suggests next steps or areas for further investigation
    """,
    "technical": """
        Generate a technical analysis report that:
        1. Focuses on technical specifications and capabilities
        2. Provides detailed architectural or system information
        3. Compares technical approaches and solutions
        4. Analyzes performance metrics and benchmarks
        5. Discusses implementation considerations
        6. Addresses technical challenges and limitations
        7. Includes code examples or technical diagrams where relevant
    """,
    "market": """
        Generate a market analysis report that:
        1. Analyzes market trends and dynamics
        2. Examines competitive landscape
        3. Identifies market opportunities and challenges
        4. Provides relevant market statistics
        5. Discusses economic factors and implications
        6. Includes customer/user insights
        7. Offers market forecasts and predictions
    """,
    "summary": """
        Generate a concise summary report that:
        1. Highlights the most important findings
        2. Presents key conclusions
        3. Outlines critical insights
        4. Provides essential recommendations
        5. Lists main action items
    """,
    # Add scientific report types
    "scientific": scientific_research_prompts["biomass_gasification"],
    "experimental": scientific_research_prompts["experimental_validation"],
    "data_extraction": scientific_research_prompts["unit_standardized"]
}

RESEARCH_ASSISTANT_SYSTEM_PROMPT = "You are a research assistant helping to gather and analyze information from web searches."

RESEARCH_PAPER_WRITER_SYSTEM_PROMPT = "You are a research paper writer synthesizing findings from web research. Use Markdown formatting and include proper citations."

QUERY_GENERATOR_SYSTEM_PROMPT = "You are a research assistant helping to generate effective follow-up search queries."

# Enhanced synthesis prompt for scientific research
SCIENTIFIC_SYNTHESIS_PROMPT = """
    Please analyze these search results focusing on EXPERIMENTAL DATA EXTRACTION:
    1. Identify papers with COMPLETE experimental sections including:
       - Feedstock type, source, and characterization
       - Operating conditions (temperature, pressure, residence time)
       - Yield data in standardized units (mol/kg, mmol/g)
       - Reactor configuration and scale
    2. Extract QUANTITATIVE DATA points with units and error bars
    3. Note METHODOLOGY QUALITY and reproducibility potential
    4. Compare UNIT REPORTING consistency across sources
    5. Identify papers suitable for RAG database integration
    6. Flag papers with INCOMPLETE or non-standard reporting
    7. Highlight sources with TABULATED DATA or appendices
    8. Note FEEDSTOCK DIVERSITY and geographic sources
    9. Assess PEER-REVIEW STATUS and journal quality
    10. Identify REVIEW PAPERS with compiled datasets
    
    Structure your analysis to:
    - Prioritize sources with complete experimental data
    - Note data extraction potential for each source
    - Identify unit conversion requirements
    - Flag papers missing critical information (feedstock, conditions, yields)
    - Recommend sources for detailed data extraction
    
    Focus on scientific rigor and data completeness over general market insights.
"""

SYNTHESIS_PROMPT = """
    Please analyze these search results and their full content to provide:
    1. Key facts and data points
    2. Expert opinions and perspectives
    3. Recent developments or trends
    4. Contrasting viewpoints or contradictions
    5. Industry-specific insights
    6. Statistical information when available
    7. Practical applications or real-world examples
    8. Technical details or specifications
    9. Potential limitations or challenges
    10. Market or domain context
    
    Structure your analysis to:
    - Highlight the most significant and reliable information
    - Note the credibility and relevance of sources
    - Identify any potential biases or limitations in the data
    - Connect new information with previous findings
    - Flag areas that need verification or deeper investigation
    
    Provide your analysis in a detailed but concise format.
"""

# Enhanced follow-up queries for scientific research
SCIENTIFIC_FOLLOW_UP_QUERIES_PROMPT = """
    Generate 3 specific follow-up search queries targeting papers with:
    1. Complete experimental data (feedstock + conditions + yields in mol/kg)
    2. Peer-reviewed methodology sections with reproducible protocols
    3. Comparative studies across multiple feedstocks or operating conditions
    
    Focus on queries that would find papers suitable for scientific RAG systems.
    Include specific biomass types, gasification technologies, and unit specifications.
    
    Return ONLY search queries that target academic sources with experimental data.
"""

FOLLOW_UP_QUERIES_PROMPT = """
    Generate 3 specific follow-up search queries that would help:
    1. Fill gaps in our current knowledge
    2. Verify important claims
    3. Explore related aspects we haven't covered
    
    Return ONLY search queries that are clear and contain no special characters.
"""

MERMAID_CHART_REQUIREMENTS = """
    When including charts or diagrams:
    - Use Mermaid markdown syntax
    - Wrap charts in ```mermaid blocks
    - Support for: flowcharts, sequence diagrams, pie charts, gantt charts
    - Keep charts simple and readable
    - Include clear labels and titles
    - Use consistent styling
    Example format:
    ```mermaid
    graph TD
        A[Start] --> B[Process]
        B --> C[End]
    ```
"""

REPORT_FORMATTING_REQUIREMENTS = f"""
    Formatting requirements:
    - Use Markdown formatting for clear structure
    - Include citations using [1], [2], etc.
    - Add a References section listing all sources
    - Use tables for comparing data where appropriate
    - Use bullet points for lists
    - Include relevant quotes when they add value
    - Break down complex information into digestible sections
    {MERMAID_CHART_REQUIREMENTS}
"""