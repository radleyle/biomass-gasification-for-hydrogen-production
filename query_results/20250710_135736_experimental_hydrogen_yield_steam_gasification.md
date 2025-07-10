# RAG Query Result

## Query Information
- **Query**: experimental hydrogen yield steam gasification
- **Timestamp**: 2025-07-10 13:57:36
- **Database**: chroma
- **Results Found**: 12

## Similarity Scores
- **1.** Score: 0.529 | Source: data/docling_md/steam/pc_3_2015_tavasoli_344.md
- **2.** Score: 0.522 | Source: data/docling_md/steam/10.1002_wene.97_final.md
- **3.** Score: 0.488 | Source: data/docling_md/steam/10.1002_wene.97_final.md
- **4.** Score: 0.476 | Source: data/docling_md/steam/pc_3_2015_tavasoli_344.md
- **5.** Score: 0.475 | Source: data/docling_md/steam/37408.md

## GPT-4 Analysis

**Experimental Data Found:**
- Technology: Steam Gasification
- Feedstock: Bagasse
- Conditions: High temperature, presence of steam
- H₂ Yield: Increase from 8.6 to 18.5 mmol/g bagasse (Source: Context Document 1)
- CO Yield: Not specified
- Other yields: Increase in CO2 yield, no significant change in CH4 and light hydrocarbons (C2H4 and C2H6) (Source: Context Document 1)

- Technology: Supercritical Water Gasification (SCWG)
- Feedstock: Not specified
- Conditions: 500 C, 90-minute reaction time
- H₂ Yield: Not specified
- CO Yield: Approximately 0.3 mol/kg (Source: Context Document 12)
- Other yields: CO2 approximately 3.6 mol/kg, CH4 approximately 2.6 mol/kg (Source: Context Document 12)

**Key Findings:**
- The presence of steam in the reaction increases the amount of gas generated from 8.6 to 18.5 mmol/g bagasse.
- The increase in the H2, CO and CO2 yield and the decrease in the methane yield can be attributed to the steam reforming and water gas shift processes.
- At a temperature of 500 C, peak carbon efficiency (CE) and total gas production were 6.8 % and 8.6 %, respectively.

**Source Reliability:**
The data is consistent across the sources, indicating a high level of reliability. However, the feedstock for the SCWG technology is not specified, which may affect the generalizability of the results.

**Missing Information:**
The specific pressure conditions for the steam gasification of bagasse are not provided. Additionally, the exact feedstock for the SCWG technology is not specified.

## Source Details
- 1. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:25
- 2. data/docling_md/steam/10.1002_wene.97_final.md:0:63
- 3. data/docling_md/steam/10.1002_wene.97_final.md:0:21
- 4. data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:4
- 5. data/docling_md/steam/37408.md:0:295
- 6. data/docling_md/scw/POLANCO_MA_CTW.md:0:179
- 7. data/docling_md/steam/37408.md:0:8
- 8. data/docling_md/scw/1-s2.0-S2590123024016840-main.md:0:78
- 9. data/docling_md/scw/1-s2.0-S2590123024016840-main.md:0:61
- 10. data/docling_md/scw/energies-16-03343.md:0:56
- 11. data/docling_md/scw/1-s2.0-S2590123024016840-main.md:0:2
- 12. data/docling_md/scw/1-s2.0-S2590123024016840-main.md:0:26

## Raw Context (First 3 Documents)

### Document 1 (Score: 0.529)
**Source**: data/docling_md/steam/pc_3_2015_tavasoli_344.md:0:25

```
The presence of steam in the reaction increased the amount of gas generated from 8.6 to 18.5 mmol/g baggase. As shown, H2, CO and CO2 yield increased but no significant change in the amount of CH4 and light hydrocarbons (C2H4 and C2H6) were observed. The increase in the H2, CO and CO2 yield and the decrease in the methane yield can be attributed to the steam reforming and water gas shift processes (Eqs. 7-10). On the other hand, steam reforming reactions are endothermic and gasification occurs a...
```

### Document 2 (Score: 0.522)
**Source**: data/docling_md/steam/10.1002_wene.97_final.md:0:63

```
The common method for hydrogen production is natural gas steam reforming, but if hydrogen should be produced from renewable, biomass gasification is probably the most economic option. The aim of the project was the production of hydrogen with high purity for the direct integration in a refinery. First, a simulation of the whole process was done. The hydrogen production was based on steam gasification, a CO-shift step, CO2-separation with a pressurized water scrubber, a PSA system, a steam reform...
```

### Document 3 (Score: 0.488)
**Source**: data/docling_md/steam/10.1002_wene.97_final.md:0:21

```
Hydrogen

Hydrogen can be produced from the gasification product gas through the steam reforming and watergas shift reaction. Using a dual fluidized bed (DFB) gasification system with CO2 adsorption along with suitable catalysts, it is possible to achieve a hydrogen yield up to 70 vol% direct in the gasifier. 11

Furthermore, the costs of hydrogen production by biomass gasification in very large scale are competitive with natural gas reforming. 12

Hydrogen is one of the most promising future en...
```
