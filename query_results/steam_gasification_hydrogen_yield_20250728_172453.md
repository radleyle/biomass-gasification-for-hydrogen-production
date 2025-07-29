# RAG Query Result

## Query Information
- **Query**: experimental hydrogen yield mmol/g mol/kg steam gasification
- **Timestamp**: 2025-07-28 17:24:53
- **Database**: chroma
- **Results Found**: 11

## Similarity Scores
- **1.** Score: 0.501 | Source: data/deep_search_results_md/applsci-15-03995.md
- **2.** Score: 0.490 | Source: data/deep_search_results_md/37408.md
- **3.** Score: 0.484 | Source: data/deep_search_results_md/catalysts-15-00280.md
- **4.** Score: 0.484 | Source: data/deep_search_results_md/applsci-15-03995.md
- **5.** Score: 0.482 | Source: data/deep_search_results_md/energies-16-03343.md

## GPT-4 Analysis

**Experimental Data Found:**

- Technology: Steam Gasification
- Feedstock: Corncob, Waste Wood, Xylose, Sewage Sludge, Bagasse (Sources: Cao et al. [77], [61,62], Gokkaya et al. [16], Chen et al. [17], [33])
- Conditions: 
  - Corncob: 650 ◦ C (Source: Cao et al. [77])
  - Waste Wood: 600 ◦ C to 800 ◦ C (Sources: [61,62])
  - Xylose: 600 ◦ C, 21 MPa, 60 min (Source: Gokkaya et al. [16])
  - Sewage Sludge: 750 ◦ C, 30 min (Source: Chen et al. [17])
  - Bagasse: Not specified (Source: [33])
- H₂ Yield: 
  - Corncob: 61.2 mmol/g (Source: Cao et al. [77])
  - Waste Wood: 10.5 mmol/g to 27.52 mmol/g (Sources: [61,62])
  - Xylose: 18 mol H2/kg (Source: Gokkaya et al. [16])
  - Sewage Sludge: Not specified (Source: Chen et al. [17])
  - Bagasse: 25.35 mmol/g (Source: [33])
- CO Yield: Not specified
- Other yields: Not specified

**Key Findings:**

- The use of steam in the gasification process significantly increases the hydrogen yield.
- Increasing the pyrolysis temperature can beneficially affect gas production and hydrogen yield in the two-stage process.
- The presence of catalysts has an influence with reaction times but did not contribute to improving the H2 yield.

**Source Reliability:**

The data is consistent across multiple sources, indicating a high level of reliability. However, the lack of specific CO yield data and other yields is a limitation.

**Missing Information:**

The specific CO yield and other yields are not provided in the context documents. Additionally, the experimental conditions for the bagasse feedstock are not specified.

## Source Details
- 1. data/deep_search_results_md/applsci-15-03995.md:0:68
- 2. data/deep_search_results_md/37408.md:0:295
- 3. data/deep_search_results_md/catalysts-15-00280.md:0:129
- 4. data/deep_search_results_md/applsci-15-03995.md:0:54
- 5. data/deep_search_results_md/energies-16-03343.md:0:56
- 6. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:25
- 7. data/deep_search_results_md/applsci-15-03995.md:0:43
- 8. data/deep_search_results_md/biomass-05-00028-v2.md:0:3
- 9. data/deep_search_results_md/energies-16-03343.md:0:36
- 10. data/deep_search_results_md/37408.md:0:225
- 11. data/deep_search_results_md/energies-16-03343.md:0:41

## Raw Context (First 3 Documents)

### Document 1 (Score: 0.501)
**Source**: data/deep_search_results_md/applsci-15-03995.md:0:68

```
by 279.8% and reached 61.9 mmol/g [76]. Another research study performed by Cao et al. [77] assessed the effects of using steam and a Ni-exchanged resin char catalyst on reforming corncob pyrolysis volatiles at 650 ◦ C. Gas yield results demonstrated that the steam reforming process produced 84.5 mmol/g of gas, 80% more than the reforming process without steam. In addition, the hydrogen yield increased to 61.2 mmol/g, which was 37 mmol/g more than that supplied by the non-steam reforming process...
```

### Document 2 (Score: 0.490)
**Source**: data/deep_search_results_md/37408.md:0:295

```
Plant Steam Use (kg steam/kg H2)

42.0

Hydrogen Production Process Engineering Analysis

Design Report: Sensitivity on Current Case - stm:wood ratio = 1 with same gasifier temperature (Case K) 2000 Dry Metric Tonnes Biomass per Day BCL Gasifier, Tar Reformer, Sulfur Removal, Methane Reformer, HTS & LTS, PSA, Steam-Power Cycle All Values in 2002$

Minimum Hydrogen Selling Price ($/kg) $1.58

Hydrogen Production at operating capacity (MM kg / year) 52.1

Hydrogen Yield (kg / Dry US Ton Feedstock)...
```

### Document 3 (Score: 0.484)
**Source**: data/deep_search_results_md/catalysts-15-00280.md:0:129

```
biomass feedstocks were almost completely converted, with hydrogen production reaching 58.6 mmol g wood ି 1 ....
```
