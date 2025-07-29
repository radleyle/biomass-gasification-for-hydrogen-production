# RAG Query Result

## Query Information
- **Query**: carbon monoxide CO yield mmol/g steam gasification
- **Timestamp**: 2025-07-29 18:54:36
- **Database**: chroma
- **Results Found**: 20

## Similarity Scores
- **1.** Score: 0.552 | Source: data/deep_search_results_md/eng-06-00012.md
- **2.** Score: 0.535 | Source: data/deep_search_results_md/pc_3_2015_tavasoli_344.md
- **3.** Score: 0.509 | Source: data/deep_search_results_md/pc_3_2015_tavasoli_344.md
- **4.** Score: 0.483 | Source: data/deep_search_results_md/pc_3_2015_tavasoli_344.md
- **5.** Score: 0.472 | Source: data/deep_search_results_md/pc_3_2015_tavasoli_344.md

## GPT-4 Analysis

**Experimental Data Found:**

- Technology: Steam Gasification
- Feedstock: Energy Sugarcane biomass, Coffee Husk Biochar, Eucalyptus Biochar, RDF (Refuse Derived Fuel)
- Conditions: 1273.15 K, 220 bar, biomass composition of 69%
- CO Yield: 0.96 mol for Energy Sugarcane biomass, 0.86 mol for Coffee Husk Biochar, 0.85 mol for Eucalyptus Biochar, and 0.85 mol for RDF (Source: Context Document 1)

- Technology: Steam Gasification
- Feedstock: Bagasse
- Conditions: 850°C, atmospheric pressure, 30 min reaction time
- CO Yield: 7.5 mmol/g bagasse (Source: Context Document 3)

**Key Findings:**

- Energy Sugarcane biomass produced the highest levels of CO formation in steam gasification, although the difference compared to other biomasses was minimal.
- The presence of steam in the reaction increased the amount of gas generated from bagasse.
- The CO yield from bagasse in steam gasification was 7.5 mmol/g.

**Source Reliability:**

The data appears to be consistent and reliable, coming from scientific research papers. However, the conditions under which the experiments were conducted vary, which may affect the comparability of the results.

**Missing Information:**

The exact source location of the biomass feedstock is not provided. Additionally, the specific experimental setup and procedure details are not fully described.

## Source Details
- 1. data/deep_search_results_md/eng-06-00012.md:0:71
- 2. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:25
- 3. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:20
- 4. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:28
- 5. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:21
- 6. data/deep_search_results_md/applsci-15-03995.md:0:68
- 7. data/deep_search_results_md/ssrn-4340869.md:0:76
- 8. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:31
- 9. data/deep_search_results_md/sustainability-17-01888.md:0:73
- 10. data/deep_search_results_md/eng-06-00012.md:0:3
- 11. data/deep_search_results_md/ssrn-4340869.md:0:68
- 12. data/deep_search_results_md/s43979-022-00043-3.md:0:41
- 13. data/deep_search_results_md/238549.md:0:11
- 14. data/deep_search_results_md/ssrn-4803744.md:0:22
- 15. data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:29
- 16. data/deep_search_results_md/eng-06-00012.md:0:54
- 17. data/deep_search_results_md/s43979-022-00043-3.md:0:31
- 18. data/deep_search_results_md/238549.md:0:80
- 19. data/deep_search_results_md/ssrn-4803744.md:0:21
- 20. data/deep_search_results_md/ssrn-4340869.md:0:69

## Raw Context (First 3 Documents)

### Document 1 (Score: 0.552)
**Source**: data/deep_search_results_md/eng-06-00012.md:0:71

```
Regarding the formation of carbon monoxide, the Energy Sugarcane biomass exhibited the highest levels of formation, although the difference compared to the other biomasses was minimal. For instance, in the CO2 gasification process at 220 bar, 1273.15 K, and a biomass composition of 69%, the Energy Sugarcane biomass produced 0.96 mol of CO, followed by 0.86, 0.85, and 0.85 mol of CO for Coffee Husk Biochar, Eucalyptus Biochar, and RDF, respectively. This trend is similar for the SCWG process. Thi...
```

### Document 2 (Score: 0.535)
**Source**: data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:25

```
The presence of steam in the reaction increased the amount of gas generated from 8.6 to 18.5 mmol/g baggase. As shown, H2, CO and CO2 yield increased but no significant change in the amount of CH4 and light hydrocarbons (C2H4 and C2H6) were observed. The increase in the H2, CO and CO2 yield and the decrease in the methane yield can be attributed to the steam reforming and water gas shift processes (Eqs. 7-10). On the other hand, steam reforming reactions are endothermic and gasification occurs a...
```

### Document 3 (Score: 0.509)
**Source**: data/deep_search_results_md/pc_3_2015_tavasoli_344.md:0:20

```
3.2 Reaction

In order to determine performance of bagasse gasification in presence of steam, two non-catalytic processes, pyrolysis and steam-gasification, were compared. Thereafter, the effects of catalyst type on the conversion, gasification yield and product gas composition were studied. All experiments were performed at the temperature of 850°C and atmospheric pressure.

3.2.1 Non-catalytic tests

Table 2 presents the non- catalytic pyrolysis and steam-gasification yields (mmol of gas/g of ...
```
