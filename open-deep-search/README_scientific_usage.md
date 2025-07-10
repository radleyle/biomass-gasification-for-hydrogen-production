# Enhanced Scientific Search for Biomass Gasification Research

## Overview
This enhanced open-deep-search tool now includes specialized modes for finding high-quality scientific papers with complete experimental data, standardized units, and comprehensive feedstock information.

## Scientific Search Modes

### 1. Scientific Mode (Default)
**Purpose**: Find peer-reviewed papers with complete experimental sections
**Targets**: Papers with feedstock + conditions + yields in the same study

```bash
python main.py "rice husk steam gasification hydrogen yield" --mode scientific
python main.py "bagasse CO2 gasification experimental data" --mode scientific  
python main.py "plasma gasification biomass yield mol/kg" --mode scientific
```

### 2. Experimental Mode
**Purpose**: Focus on reproducible protocols and methodology validation
**Targets**: Papers with detailed experimental protocols and quality control

```bash
python main.py "supercritical water gasification methodology" --mode experimental
python main.py "fluidized bed gasification reactor design" --mode experimental
```

### 3. Data Extraction Mode
**Purpose**: Find papers with standardized units and tabulated data
**Targets**: Papers reporting yields in mol/kg, mmol/g with clear data tables

```bash
python main.py "hydrogen yield mol/kg gasification comparison" --mode data_extraction
python main.py "biomass gasification yield units mmol/g" --mode data_extraction
```

## Key Improvements for RAG Systems

### Enhanced Search Targeting
- **Standardized Units**: Prioritizes mol/kg, mmol/g reporting
- **Complete Experimental Sections**: Finds papers with feedstock + conditions + yields
- **Peer-Reviewed Sources**: Targets established journals with quality control
- **Tabulated Data**: Emphasizes papers with extractable data tables

### Better Paper Quality
- **Reproducible Methodologies**: Clear experimental protocols
- **Feedstock Characterization**: Detailed biomass specifications and sources
- **Comprehensive Results**: Multiple operating conditions and comparative data
- **Recent Publications**: 2015-2024 timeframe for current methodologies

## Example Commands for RAG Database Building

### Steam Gasification Research
```bash
# Get comprehensive experimental data
python main.py "steam gasification hydrogen yield mol/kg experimental data" --mode scientific

# Focus on methodology validation  
python main.py "steam gasification reactor design methodology" --mode experimental

# Target standardized data tables
python main.py "biomass steam gasification yield comparison table" --mode data_extraction
```

### CO2 Gasification Research
```bash
python main.py "CO2 gasification supercritical biomass experimental yield" --mode scientific
python main.py "carbon dioxide gasification methodology reactor" --mode experimental  
python main.py "CO2 gasification yield mol/kg data table" --mode data_extraction
```

### Plasma Gasification Research
```bash
python main.py "plasma gasification biomass hydrogen yield experimental" --mode scientific
python main.py "plasma gasification reactor methodology validation" --mode experimental
python main.py "plasma gasification yield mmol/g standardized units" --mode data_extraction
```

## Integration with RAG Pipeline

### Step 1: Enhanced Paper Discovery
```bash
# Use scientific mode to find high-quality papers
python main.py "your_gasification_topic" --mode scientific --max-steps 7
```

### Step 2: Extract Better Papers
- Results saved to `deep_search_results/scientific_your_topic.md`
- Papers will have complete experimental sections
- Feedstock and yield data more likely to be co-located

### Step 3: Improved RAG Database
- Convert better papers to markdown using docling
- Populate database with higher-quality, unit-standardized content
- Reduced feedstock specification issues

## Expected Benefits

### For RAG System
- **Reduced "feedstock unspecified" issues**: Papers include complete experimental sections
- **Better unit consistency**: Targeted search for mol/kg, mmol/g reporting
- **Improved chunking**: Materials/methods and results sections from same papers
- **Higher data quality**: Peer-reviewed sources with validated methodologies

### For Research Quality
- **Reproducible Results**: Clear experimental protocols and conditions
- **Comparative Analysis**: Multiple feedstocks and operating conditions
- **Data Reliability**: Error analysis and statistical validation
- **Current Methodologies**: Recent publications with modern techniques

## Usage Tips

1. **Include specific feedstock terms** in your search queries for best results
2. **Use --max-steps 7-10** for comprehensive coverage of literature
3. **Combine with existing RAG queries** to validate and expand your database
4. **Review the generated reports** to identify the highest-quality sources for detailed extraction

This enhanced search system should significantly improve the quality of papers feeding into your RAG database, leading to more complete experimental data extraction with proper feedstock identification. 