# Machine Learning-Driven Framework for Life Cycle Assessment and Optimization of Hydrogen Production Technologies

## Overview
This project focuses on evaluating and comparing the environmental sustainability of biomass gasification technologies for hydrogen production through Life Cycle Assessment (LCA). The framework analyzes four promising gasification pathways:
- Steam Gasification
- Supercritical Water Gasification (SCWG)
- Plasma Gasification
- CO₂ Gasification

## Methodology
The LCA is conducted using:
- **Software**: openLCA
- **Database**: ecoinvent 3.7.1 cutoff unit regionalized database
- **Data Sources**: Scholarly and institutional sources

## Project Structure
```
biomass-gasification-for-hydrogen-production/
├── data/                      # Input data and reference datasets
│   ├── docling_md/           # Processed markdown documents
│   ├── raw/                  # Original PDF research papers
│   └── LCA/                  # LCA results and data
├── models/                    # LCA models and configurations
│   └── rag_pipeline.ipynb    # RAG system development notebook
├── benchmark/                 # Testing and evaluation
│   └── test.py               # Comprehensive test suite
├── plot/                     # Visualization scripts
│   └── LCAResultsWithWaste.py # LCA results visualization
├── chroma/                   # Vector database storage
├── query_data.py             # Main RAG query interface
├── populate_database.py      # Database population script
├── create_database.py        # Database creation script
└── requirements.txt          # Python dependencies
```

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

## Usage

### 1. Database Setup and Population

#### Create and populate the vector database:
```bash
# Create the initial database structure
python create_database.py

# Populate with documents from data/docling_md/
python populate_database.py
```

### 2. Querying the RAG System

#### Interactive query interface:
```bash
python query_data.py
```

#### Programmatic usage:
```python
from query_data import query_rag

# Ask questions about the research data
response = query_rag("What is the hydrogen yield at 500°C?")
print(response)
```

### 3. Running Benchmarks and Tests

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

### 4. LCA Results Visualization

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

### 5. Data Analysis and Development

#### Jupyter notebook for RAG development:
```bash
jupyter notebook models/rag_pipeline.ipynb
```

#### Compare embedding functions:
```bash
python compare_embeddings.py
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
   python populate_database.py
   ```

## Development

### Adding New Documents
1. Place PDF files in `data/raw/[category]/`
2. Convert to markdown (using docling or similar)
3. Place markdown files in `data/docling_md/[category]/`
4. Run `python populate_database.py` to update the database

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

