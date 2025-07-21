# Open Access RAG System for Biomass Gasification Research

## Overview

This enhanced RAG (Retrieval-Augmented Generation) system is specifically designed to work with **free, open access sources** instead of expensive paywall content like ScienceDirect. It focuses on:

- **Web of Science** (free abstracts and some full texts)
- **ResearchGate** (free publications and preprints)
- **arXiv** (free preprints)
- **PubMed** (free abstracts and some full texts)
- **Other open access journals** (PLOS, Frontiers, etc.)

## Why Open Access?

Traditional scientific databases like ScienceDirect, Springer, and Wiley often require expensive institutional subscriptions. This system prioritizes free sources that are accessible to everyone, making research more democratic and cost-effective.

## New Search Modes

### 1. `web_of_science_only` (Default)
- Searches only Web of Science database
- Access to high-quality peer-reviewed content
- Free abstracts and some open access full texts
- Highest quality scientific literature

### 2. `open_access`
- Searches across all open access sources
- Prioritizes Web of Science, then ResearchGate, arXiv, PubMed
- Excludes paywall sources like ScienceDirect

### 3. `researchgate_only`
- Focuses exclusively on ResearchGate publications
- Good for finding preprints and open access papers
- Many researchers share full papers here
- Secondary priority after Web of Science

### 4. `scientific` (Original)
- General scientific search with experimental focus
- Still filters out paywalls but less restrictive

### 5. `experimental`
- Focuses on reproducible protocols
- Good for methodology validation

### 6. `data_extraction`
- Targets standardized units (mol/kg, mmol/g)
- Ideal for extracting numerical data

## Installation and Setup

### 1. Environment Variables
Create a `.env` file in the project root:

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
FIRECRAWL_API_KEY=your_firecrawl_key_here

# Optional settings
AI_MODEL=gpt-4o
SEARCH_COUNTRY=us
SEARCH_LANG=en
SEARCH_DATE_RANGE=lastYear
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Quick Test
Test the open access functionality:

```bash
cd open-deep-search
python test_open_access.py
```

### Single Query Search
Search for specific topics using open access sources:

```bash
# Web of Science only (default)
python main.py "steam gasification biomass hydrogen yield" --mode web_of_science_only

# Open access mode (Web of Science priority)
python main.py "supercritical water gasification temperature effect" --mode open_access

# ResearchGate only
python main.py "plasma gasification efficiency" --mode researchgate_only
```

### Train the RAG Model
Train the system on a comprehensive dataset:

```bash
python train_open_access_rag.py
```

This will:
- Process 30+ queries across different gasification types
- Collect data from open access sources only
- Save training data to `open_access_training_data/`
- Generate comprehensive reports

## Training Data Structure

The training script processes queries in these categories:

### Gasification Technologies
- **Steam Gasification**: 5 queries
- **Supercritical Water Gasification**: 5 queries  
- **Plasma Gasification**: 5 queries
- **CO2 Gasification**: 5 queries

### Analysis Types
- **Environmental Impact**: 5 queries (LCA, emissions, sustainability)
- **Economic Analysis**: 5 queries (cost, feasibility, commercialization)

## Output Files

### Training Data
- `open_access_training_data/complete_dataset_YYYYMMDD_HHMMSS.json`
- `open_access_training_data/open_access_YYYYMMDD_HHMMSS.json`
- `open_access_training_data/training_summary_YYYYMMDD_HHMMSS.json`

### Search Results
- `query_results/` directory contains individual search results
- Each file named with timestamp and query description

## Source Prioritization

The system automatically prioritizes sources in this order:

### 🌟 Priority Sources (Open Access)
1. **Web of Science** - Free abstracts, some full texts (highest quality)
2. **ResearchGate** - Free publications, preprints (secondary)
3. **arXiv** - Free preprints
4. **PubMed** - Free abstracts, some full texts
5. **PLOS, Frontiers, Hindawi** - Open access journals
6. **Nature, Science** - Open access articles only

### ⏭️ Excluded Sources (Paywalls)
- ScienceDirect (expensive)
- Springer chapters (paid)
- Wiley abstracts only (paid)
- JSTOR (often behind paywall)
- Emerald (often behind paywall)

## Benefits

### 1. Cost-Effective
- No expensive institutional subscriptions needed
- Access to high-quality research for free
- Democratizes access to scientific literature

### 2. Comprehensive Coverage
- Covers all major gasification technologies
- Includes environmental and economic analysis
- Focuses on experimental data and methodology

### 3. Quality Assurance
- Prioritizes peer-reviewed content
- Filters for experimental data and standardized units
- Excludes low-quality or paywall sources

### 4. Reproducible Research
- All sources are accessible to everyone
- Methodology can be replicated by other researchers
- Transparent data collection process

## Example Queries

### Steam Gasification
```bash
python main.py "steam gasification biomass hydrogen yield experimental data" --mode open_access
```

### Supercritical Water Gasification
```bash
python main.py "supercritical water gasification temperature pressure optimization" --mode researchgate_only
```

### Environmental Impact
```bash
python main.py "biomass gasification environmental impact LCA greenhouse gas emissions" --mode open_access
```

### Economic Analysis
```bash
python main.py "biomass gasification economic feasibility cost analysis hydrogen production" --mode web_of_science_only
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure all required API keys are in `.env` file
   - Check that keys are valid and have sufficient credits

2. **No Results Found**
   - Try different search modes
   - Broaden the search query
   - Check if the topic has open access literature

3. **Rate Limiting**
   - The system includes delays between requests
   - If you hit rate limits, wait and try again

### Performance Tips

1. **Use Specific Modes**
   - `researchgate_only` for preprints and free papers
   - `web_of_science_only` for high-quality abstracts
   - `open_access` for comprehensive coverage

2. **Optimize Queries**
   - Include specific terms like "experimental data"
   - Add units like "mol/kg" or "mmol/g"
   - Specify gasification type clearly

3. **Batch Processing**
   - Use `train_open_access_rag.py` for comprehensive training
   - Results are saved automatically after each query

## Future Enhancements

1. **Additional Sources**
   - Google Scholar (free)
   - DOAJ (Directory of Open Access Journals)
   - Institutional repositories

2. **Enhanced Filtering**
   - Publication date filtering
   - Citation count prioritization
   - Author reputation scoring

3. **Integration**
   - Direct integration with your existing RAG pipeline
   - Automated data extraction from PDFs
   - Real-time literature monitoring

## Contributing

To add new open access sources or improve the filtering:

1. Edit `preferred_domains` in `web_research_agent.py`
2. Add new search modes in `set_scientific_mode()`
3. Update query enhancement in `enhance_query_for_scientific_mode()`
4. Test with `test_open_access.py`

This open access approach ensures your research is based on freely available literature, making it more accessible and reproducible for the broader scientific community. 