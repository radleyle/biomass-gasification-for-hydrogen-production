# RAG Query Result

## Query Information
- **Query**: hydrogen yield mmol/g steam gasification
- **Timestamp**: 2025-07-10 14:39:17
- **Database**: chroma
- **Results Found**: 12

## Similarity Scores
- **1.** Score: 0.521 | Source: data/docling_md/steam/pc_3_2015_tavasoli_344.md
- **2.** Score: 0.471 | Source: data/docling_md/steam/37408.md
- **3.** Score: 0.435 | Source: data/docling_md/steam/37408.md
- **4.** Score: 0.414 | Source: data/docling_md/steam/37408.md
- **5.** Score: 0.404 | Source: data/docling_md/steam/10.1002_wene.97_final.md

## GPT-4 Analysis

**Experimental Data Found:**
- Technology: Steam Gasification
- Feedstock: Bagasse (as mentioned in the context documents)
- Conditions: Temperature of 850°C, atmospheric pressure, reaction time of 30 min, bagasse loading of 1g, water flow rate of 0.6 ml/min.
- H₂ Yield: 9 mmol/g bagasse (Source: Table 2 in the context documents)
- CO Yield: 7.5 mmol/g bagasse (Source: Table 2 in the context documents)
- Other yields: CO2 Yield: 1 mmol/g bagasse, CH4 Yield: 0.6 mmol/g bagasse, Heavier Hydrocarbon Yield: 0.09 mmol/g bagasse (Source: Table 2 in the context documents)

**Key Findings:**
- The presence of steam in the reaction increased the amount of gas generated from 8.6 to 18.5 mmol/g bagasse.
- The increase in the H2, CO and CO2 yield and the decrease in the methane yield can be attributed to the steam reforming and water gas shift processes.
- The carbon conversion efficiency (ηc) and the dry heating value (LHV) of the product gas in the presence of steam increased.

**Source Reliability:**
The data appears to be consistent and reliable as it is extracted from scientific research papers. However, the data is specific to the conditions and feedstock used in the experiments and may vary under different conditions or with different feedstocks.

**Missing Information:**
The specific source location of the bagasse feedstock is not mentioned in the context documents.

## Source Details
- 1. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:25
- 2. data/docling_md/steam/37408.md:0:295
- 3. data/docling_md/steam/37408.md:0:280
- 4. data/docling_md/steam/37408.md:0:340
- 5. data/docling_md/steam/10.1002_wene.97_final.md:0:9
- 6. data/docling_md/steam/10.1002_wene.97_final.md:0:21
- 7. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:21
- 8. data/docling_md/steam/37408.md:0:8
- 9. data/docling_md/steam/10.1002_wene.97_final.md:0:63
- 10. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:20
- 11. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:4
- 12. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:1

## Raw Context (First 3 Documents)

### Document 1 (Score: 0.521)
**Source**: data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:25

```
The presence of steam in the reaction increased the amount of gas generated from 8.6 to 18.5 mmol/g baggase. As shown, H2, CO and CO2 yield increased but no significant change in the amount of CH4 and light hydrocarbons (C2H4 and C2H6) were observed. The increase in the H2, CO and CO2 yield and the decrease in the methane yield can be attributed to the steam reforming and water gas shift processes (Eqs. 7-10). On the other hand, steam reforming reactions are endothermic and gasification occurs a...
```

### Document 2 (Score: 0.471)
**Source**: data/docling_md/steam/37408.md:0:295

```
Plant Steam Use (kg steam/kg H2)

42.0

Hydrogen Production Process Engineering Analysis

Design Report: Sensitivity on Current Case - stm:wood ratio = 1 with same gasifier temperature (Case K) 2000 Dry Metric Tonnes Biomass per Day BCL Gasifier, Tar Reformer, Sulfur Removal, Methane Reformer, HTS & LTS, PSA, Steam-Power Cycle All Values in 2002$

Minimum Hydrogen Selling Price ($/kg) $1.58

Hydrogen Production at operating capacity (MM kg / year) 52.1

Hydrogen Yield (kg / Dry US Ton Feedstock)...
```

### Document 3 (Score: 0.435)
**Source**: data/docling_md/steam/37408.md:0:280

```
Plant Steam Use (kg steam/kg H2)

22.8

Hydrogen Production Process Engineering Analysis

Design Report: Sensitivity on Current Case - no dryer (Case H)

2000 Dry Metric Tonnes Biomass per Day

BCL Gasifier, Tar Reformer, Sulfur Removal, Methane Reformer, HTS & LTS, PSA, Steam-Power Cycle All Values in 2002$

Minimum Hydrogen Selling Price ($/kg) $1.78

Hydrogen Production at operating capacity (MM kg / year)

51.3

Hydrogen Yield (kg / Dry US Ton Feedstock)

66.4

Delivered Feedstock Cost $/Dry...
```
