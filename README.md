# Machine Learning-Driven Framework for Life Cycle Assessment and Optimization of Hydrogen Production Technologies

## Overview
This project focuses on evaluating and comparing the environmental sustainability of biomass gasification technologies for hydrogen production through Life Cycle Assessment (LCA) and advanced Retrieval-Augmented Generation (RAG). The framework analyzes four promising gasification pathways:
- Steam Gasification
- Supercritical Water Gasification (SCWG)
- Plasma Gasification
- CO₂ Gasification

## Methodology
The LCA is conducted using:
- **Software**: openLCA
- **Database**: ecoinvent 3.7.1 cutoff unit regionalized database
- **Data Sources**: Scholarly and institutional sources
- **AI Enhancement**: GPT-4 powered RAG system for experimental data extraction

## Project Structure
```
biomass-gasification-for-hydrogen-production/
├── data/                      # Input data and reference datasets
│   ├── docling_md/           # Processed markdown documents
│   ├── raw/                  # Original PDF research papers
│   │   ├── co2/              # CO₂ gasification papers (3 papers)
│   │   ├── steam/            # Steam gasification papers (5 papers)
│   │   ├── plasma/           # Plasma gasification papers (3 papers)
│   │   └── scw/              # Supercritical water gasification papers (4 papers)
│   └── LCA/                  # LCA results and data
├── models/                    # LCA models and configurations
│   └── rag_pipeline.ipynb    # RAG system development notebook
├── benchmark/                 # Testing and evaluation
│   └── test.py               # Comprehensive test suite
├── plot/                     # Visualization scripts
│   └── LCAResultsWithWaste.py # LCA results visualization
├── chroma/                   # Vector database storage
├── query_results/            # Saved RAG query results and documentation
├── open-deep-search/         # Web research agent for finding papers
├── query_data.py             # Enhanced RAG query interface with GPT-4
├── populate_database.py      # PDF database population script
├── populate_database_markdown.py # Markdown database population script
├── get_embedding_function.py # Configurable embedding models
├── create_database.py        # Database creation script
└── requirements.txt          # Python dependencies
```

## Available Research Data

The project includes curated research papers for four biomass gasification technologies:

| Technology | Directory | Papers | Focus Areas |
|------------|-----------|--------|-------------|
| **CO₂ Gasification** | `data/raw/co2/` | 3 papers | Carbon dioxide as gasifying agent, temperature ranges 700-900°C |
| **Steam Gasification** | `data/raw/steam/` | 5 papers | Steam reforming, hydrogen yield optimization, reactor designs |
| **Plasma Gasification** | `data/raw/plasma/` | 3 papers | Thermal plasma processes, syngas production, high-temperature reactions |
| **Supercritical Water** | `data/raw/scw/` | 4 papers | SCWG processes, supercritical conditions, reactor performance |

Each directory contains peer-reviewed research papers in PDF format that can be loaded into the RAG system for analysis and comparison.

## Installation

### Prerequisites
- Python 3.12+
- conda or pip package manager
- Ollama (for local LLM inference)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd biomass-gasification-for-hydrogen-production
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or using conda:
   ```bash
   conda install --solver=classic pytest -y
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```bash
   # Install Ollama (macOS/Linux)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull required models
   ollama pull mistral
   ollama pull nomic-embed-text
   ```

4. **Configure API Keys (Optional - for enhanced features)**
   ```bash
   # Create .env file for OpenAI integration
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "FIRECRAWL_API_KEY=your_firecrawl_api_key_here" >> .env
   ```

## Enhanced RAG System

The project features a state-of-the-art RAG system optimized for scientific data extraction:

### **Dual Model Support**
- **Local Models**: Ollama (Mistral + nomic-embed-text) - Free, private, fast
- **Cloud Models**: OpenAI (GPT-4 + text-embedding-3-large) - Research-grade accuracy

### **Scientific Data Extraction**
- **Structured prompts** for experimental data extraction
- **Unit-aware parsing** (mol/kg, mmol/g, vol%, etc.)
- **Experimental condition extraction** (temperature, pressure, time)
- **Source reliability assessment** and quality control

### **Research Documentation**
- **Automatic saving** of all query results to markdown files
- **Similarity score tracking** for quality assessment
- **Complete source attribution** with chunk-level references
- **Timestamp tracking** for research audit trails

### **Web Research Integration**
- **Open Deep Search** agent for finding unit-standardized papers
- **Technology-specific searches** for experimental data
- **Automated paper discovery** with consistent unit reporting

## Usage

### 1. Database Setup and Population

#### PDF Document Loading (Original Method):
```bash

# Populate with PDF documents from specific technology directories
python populate_database.py --data-path "data/raw/co2"      # Load CO₂ gasification papers
python populate_database.py --data-path "data/raw/steam"    # Load steam gasification papers  
python populate_database.py --data-path "data/raw/plasma"   # Load plasma gasification papers
python populate_database.py --data-path "data/raw/scw"      # Load supercritical water papers

# Reset database and load fresh data
python populate_database.py --reset --data-path "data/raw/co2"
```

#### Markdown Document Loading (Enhanced Method):
```bash
# Load markdown documents (better for experimental data extraction)
python populate_database_markdown.py --reset --data-path "data/docling_md/steam"
python populate_database_markdown.py --data-path "data/docling_md/co2"
python populate_database_markdown.py --data-path "data/docling_md/plasma"
python populate_database_markdown.py --data-path "data/docling_md/scw"
```

### 2. Enhanced RAG Query System

#### Basic Query Interface:
```bash
# Clean, professional output (default)
python query_data.py "experimental hydrogen yield mmol/g bagasse steam gasification"

# Detailed debugging output
python query_data.py "experimental hydrogen yield mmol/g bagasse steam gasification" --verbose
```

#### Query Results Features:
- **Automatic saving** to `query_results/TIMESTAMP_query.md`
- **Similarity score assessment** (>0.5 = high quality)
- **Structured experimental data extraction**
- **Source reliability evaluation**
- **Complete research documentation**

#### Example Scientific Queries:
```bash
# Unit-specific experimental data
python query_data.py "Find experimental Table results showing H2 yield with numerical values in mol/kg"
python query_data.py "steam gasification experimental yields mol/kg mmol/g biomass"

# Technology comparisons
python query_data.py "Compare hydrogen yields between steam and CO2 gasification"
python query_data.py "gasification temperature effects hydrogen yield experimental"

# Condition-specific data
python query_data.py "gasification temperature 800 850 900 experimental yields"
python query_data.py "catalytic gasification hydrogen yield experimental mmol/g"
```

#### Programmatic Usage:
```python
from query_data import query_rag

# Basic query
response = query_rag("What is the hydrogen yield at 850°C?")
print(response)

# With verbose output
response = query_rag("experimental hydrogen yield", verbose=True)
```

### 3. Web Research Agent (Open Deep Search)

#### Find Unit-Standardized Papers:
```bash
cd open-deep-search

# Technology-specific searches for consistent units
python main.py "CO2 gasification hydrogen yield mol/kg experimental results"
python main.py "steam gasification carbon monoxide CO yield mol/kg experimental"
python main.py "plasma gasification hydrogen yield mol/kg experimental"
python main.py "supercritical water gasification hydrogen yield mol/kg experimental"
```

#### Research Campaign Results:
- **Comprehensive reports** saved as markdown files
- **Source quality assessment** from top journals
- **Unit consistency validation** across papers
- **Download recommendations** for database enhancement

### 4. Model Configuration

#### Embedding Model Selection:
```python
# Edit get_embedding_function.py to choose embedding model:

# Option 1: OpenAI embeddings (best for scientific content)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")  # Highest quality
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # Good balance

# Option 2: Local Ollama embeddings (free, private)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
```

#### LLM Model Selection:
```python
# In query_data.py, choose your LLM:

# Option 1: GPT-4 (research-grade scientific reasoning)
model = ChatOpenAI(model="gpt-4", temperature=0)

# Option 2: Local Ollama (free, private)
model = OllamaLLM(model="mistral")
```

### 5. Running Benchmarks and Tests

#### Run all benchmark tests:
```bash
# Run tests with verbose output and show print statements
python -m pytest benchmark/test.py -v -s

# Run specific test categories
python -m pytest benchmark/test.py -k "edge_case" -v -s
python -m pytest benchmark/test.py -k "boundary" -v -s

# Run a single test
python -m pytest benchmark/test.py::test_hydrogen_yield_peak_temperature -v -s
```

#### Test categories included:
- **Basic functionality tests**: Core RAG system accuracy
- **Boundary value tests**: Edge cases with different parameters
- **Error handling tests**: Malformed inputs and missing data
- **Comparative analysis tests**: Complex multi-parameter queries

### 6. LCA Results Visualization

#### Generate pie charts for environmental impact analysis:
```bash
cd plot
python LCAResultsWithWaste.py
```

#### Options available:
1. **All pie charts**: Generate charts for all 18 impact categories
2. **Single pie chart**: Interactive selection of specific categories
3. **Overall comparison**: Summary comparison across all technologies
4. **Complete analysis**: All visualizations at once

#### Output:
- Individual pie charts saved to `plots/pie_charts/`
- Summary comparison saved to `plots/overall_comparison.png`
- High-resolution PNG files (300 DPI)

### 7. Data Analysis and Development

#### Jupyter notebook for RAG development:
```bash
jupyter notebook models/rag_pipeline.ipynb
```

#### Compare embedding functions:
```bash
python compare_embeddings.py
```

## Common Research Workflows

### Single Technology Analysis
```bash
# Focus on CO₂ gasification research
python populate_database.py --reset --data-path "data/raw/co2"
python query_data.py "What are the typical operating temperatures for CO₂ gasification?"
```

### Technology Comparison
```bash
# Load multiple technologies for comparative analysis
python populate_database.py --reset --data-path "data/raw/steam"
python populate_database.py --data-path "data/raw/co2"
python query_data.py "Compare hydrogen yields between steam and CO₂ gasification"
```

### Comprehensive Database
```bash
# Build complete database with all technologies
python populate_database.py --reset --data-path "data/raw/co2"
python populate_database.py --data-path "data/raw/steam"
python populate_database.py --data-path "data/raw/plasma"
python populate_database.py --data-path "data/raw/scw"
python query_data.py "Which gasification technology produces the highest hydrogen yield?"
```

### Help and Options
```bash
# View all available options
python populate_database.py --help
```

## Key Features

### RAG (Retrieval Augmented Generation) System
- **Vector Database**: ChromaDB with semantic search
- **Embeddings**: Ollama nomic-embed-text model
- **LLM**: Mistral via Ollama for response generation
- **Document Processing**: Automated PDF to markdown conversion

### Comprehensive Testing Suite
- **Accuracy Testing**: Validates specific technical data retrieval
- **Edge Case Testing**: Handles malformed and boundary inputs
- **Performance Benchmarking**: Response time and quality metrics
- **Color-coded Results**: Visual feedback for test outcomes

### Environmental Impact Visualization
- **18 Impact Categories**: Complete LCA analysis
- **4 Technologies**: Steam, SCWG, Plasma, CO₂ gasification
- **Professional Charts**: Publication-ready visualizations
- **Comparative Analysis**: Technology performance ranking

## Example Queries

### Technical Data Queries
```python
# Specific parameter queries
query_rag("What is the hydrogen yield at peak gasification temperature of 500°C?")
query_rag("What is the capacity of the SWGR batch reactor used in the study?")

# Comparative analysis
query_rag("Which temperature gives the highest hydrogen yield: 400°C, 450°C, or 500°C?")
query_rag("Compare the efficiency of different gasification technologies")
```

### Running Specific Scripts

#### Query specific research data:
```bash
python -c "from query_data import query_rag; print(query_rag('What are the three gasification temperatures tested?'))"
```

#### Test system robustness:
```bash
python -c "from query_data import query_rag; print(query_rag('What is the yield at 600°C?'))"  # Non-existent data
```

## Troubleshooting

### Common Issues

1. **"No module named pytest"**
   ```bash
   conda install --solver=classic pytest -y
   ```

2. **"Excel file not found"**
   - Ensure you're running LCA visualization from the correct directory
   - Check that `data/LCA/LCAResultsWithWaste.xlsx` exists

3. **Ollama connection errors**
   ```bash
   # Start Ollama service
   ollama serve
   
   # Verify models are available
   ollama list
   ```

4. **ChromaDB issues**
   ```bash
   # Reset database if corrupted
   rm -rf chroma/
   python create_database.py
   python populate_database.py --data-path "data/raw/co2"  # Or your preferred directory
   
   # Alternative: Use the built-in reset flag
   python populate_database.py --reset --data-path "data/raw/co2"
   ```

## Development

### Adding New Documents
1. Place PDF files in `data/raw/[category]/` (where category is co2, steam, plasma, or scw)
2. Run `python populate_database.py --data-path "data/raw/[category]"` to update the database
   - The system will automatically load all PDF files from the specified directory
   - Example: `python populate_database.py --data-path "data/raw/co2"`
3. For completely new technology categories, create a new subdirectory under `data/raw/`

### Adding New Tests
1. Edit `benchmark/test.py`
2. Follow the existing pattern for test functions
3. Use helper functions: `query_and_validate()`, `query_and_validate_flexible()`, `query_and_validate_contains()`

## Requirements
- Python 3.12+
- Ollama with mistral and nomic-embed-text models
- Required Python packages (see requirements.txt)
- 8GB+ RAM recommended for local LLM inference

## License
[radleyle 2025]

