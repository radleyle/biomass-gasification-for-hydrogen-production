#!/usr/bin/env python3
"""
Extract experimental gasification data from query result markdown files and generate CSV.

This script parses the GPT-4 analysis sections from query result files and extracts:
- Technology type (steam, CO2, plasma, SCW gasification)
- Feedstock information
- Experimental conditions (temperature, pressure, time)
- Yield data (H2, CO, CO2, CH4) with unit conversion
- Study references

Output format matches gasification_data_refined.csv structure.
"""

import os
import re
import pandas as pd
import glob
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

class GasificationDataExtractor:
    def __init__(self, query_results_dir: str = "query_results"):
        self.query_results_dir = query_results_dir
        self.extracted_data = []
        
        # Unit conversion factors to mol/kg
        self.unit_conversions = {
            'mmol/g': 1.0,      # mmol/g = mol/kg
            'mol/kg': 1.0,      # already in target units
            'mol/g': 1000.0,    # mol/g to mol/kg
            'mmol/kg': 0.001,   # mmol/kg to mol/kg
            'mol': 1.0,         # assume mol/kg when just "mol"
            'mmol': 0.001,      # assume mmol/kg when just "mmol"
        }
        
        # Technology mapping
        self.tech_mapping = {
            'steam gasification': 'steam',
            'steam': 'steam',
            'co2 gasification': 'co2',
            'co₂ gasification': 'co2',
            'carbon dioxide gasification': 'co2',
            'plasma gasification': 'plasma',
            'plasma': 'plasma',
            'supercritical water gasification': 'scw',
            'scw gasification': 'scw',
            'scw': 'scw',
            'supercritical water': 'scw'
        }
        
        # Common feedstock standardization
        self.feedstock_mapping = {
            'rice husk': 'rice_husk',
            'rice hull': 'rice_husk',
            'bagasse': 'bagasse',
            'sugar cane bagasse': 'bagasse',
            'sawdust': 'sawdust',
            'wood dust': 'sawdust',
            'wood saw dust': 'sawdust',
            'wood chips': 'wood_chips',
            'wooden pellets': 'wood_pellets',
            'wood pellets': 'wood_pellets',
            'corncob': 'corn_cob',
            'corn stover': 'corn_stover',
            'wheat straw': 'wheat_straw',
            'xylose': 'xylose',
            'kraft lignin': 'kraft_lignin',
            'timothy grass': 'timothy_grass',
            'food waste': 'food_waste',
            'municipal solid waste': 'municipal_waste',
            'msw': 'municipal_waste',
            'sewage sludge': 'sewage_sludge',
            'sludge': 'sewage_sludge',
            'biomass': 'biomass',
            'waste wood': 'waste_wood',
            'plastic waste': 'plastic_waste',
            'hdpe': 'hdpe',
            'ffp2 plastic feedstock': 'plastic_waste'
        }

    def extract_from_markdown(self, filepath: str) -> List[Dict]:
        """Extract experimental data from a single markdown file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find GPT-4 Analysis section
        analysis_match = re.search(r'## GPT-4 Analysis\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if not analysis_match:
            print(f"⚠️  No GPT-4 Analysis found in {filepath}")
            return []
        
        analysis_text = analysis_match.group(1)
        
        # Extract experimental data section
        exp_data_match = re.search(r'\*\*Experimental Data Found:\*\*(.*?)(?=\*\*|$)', analysis_text, re.DOTALL)
        if not exp_data_match:
            print(f"⚠️  No experimental data section found in {filepath}")
            return []
        
        exp_data_text = exp_data_match.group(1)
        
        # Extract basic information
        technology = self._extract_technology(exp_data_text)
        feedstocks = self._extract_feedstocks(exp_data_text)
        
        # Extract yield data
        h2_yields = self._extract_yields(exp_data_text, ['H₂ Yield', 'H2 Yield', 'Hydrogen Yield'])
        co_yields = self._extract_yields(exp_data_text, ['CO Yield', 'Carbon Monoxide Yield'])
        co2_yields = self._extract_yields(exp_data_text, ['CO2 Yield', 'CO₂ Yield'])
        ch4_yields = self._extract_yields(exp_data_text, ['CH4 Yield', 'CH₄ Yield', 'Methane Yield'])
        
        # Extract conditions
        conditions = self._extract_conditions(exp_data_text)
        
        # Create data entries
        extracted_entries = []
        
        # If we have specific yield data per feedstock
        if any([h2_yields, co_yields, co2_yields, ch4_yields]):
            # Create entries for each unique combination
            all_yields = {**h2_yields, **co_yields, **co2_yields, **ch4_yields}
            feedstock_keys = set()
            
            for yield_dict in [h2_yields, co_yields, co2_yields, ch4_yields]:
                feedstock_keys.update(yield_dict.keys())
            
            for feedstock_key in feedstock_keys:
                entry = self._create_entry_template(technology, filepath)
                entry['feedstock_type'] = self._standardize_feedstock(feedstock_key)
                
                # Add yields (handle both mol/kg and percentage values)
                entry['H2_yield_mol_kg'] = self._format_yield_value(h2_yields.get(feedstock_key, ''))
                entry['CO_yield_mol_kg'] = self._format_yield_value(co_yields.get(feedstock_key, ''))
                entry['CO2_yield_mol_kg'] = self._format_yield_value(co2_yields.get(feedstock_key, ''))
                entry['CH4_yield_mol_kg'] = self._format_yield_value(ch4_yields.get(feedstock_key, ''))
                
                # Add conditions if available for this feedstock
                if feedstock_key in conditions:
                    cond = conditions[feedstock_key]
                    entry.update(cond)
                
                extracted_entries.append(entry)
        
        else:
            # Create single entry if no specific yield data
            entry = self._create_entry_template(technology, filepath)
            entry['feedstock_type'] = ', '.join([self._standardize_feedstock(f) for f in feedstocks]) if feedstocks else 'unknown'
            extracted_entries.append(entry)
        
        return extracted_entries

    def _extract_technology(self, text: str) -> str:
        """Extract gasification technology type."""
        tech_match = re.search(r'- Technology:\s*(.+)', text, re.IGNORECASE)
        if tech_match:
            tech_text = tech_match.group(1).lower().strip()
            for key, value in self.tech_mapping.items():
                if key in tech_text:
                    return value
        return 'unknown'

    def _extract_feedstocks(self, text: str) -> List[str]:
        """Extract feedstock types."""
        feedstock_match = re.search(r'- Feedstock:\s*(.+)', text, re.IGNORECASE)
        if feedstock_match:
            feedstock_text = feedstock_match.group(1)
            # Split by commas and clean up
            feedstocks = [f.strip() for f in feedstock_text.split(',')]
            # Remove source references
            feedstocks = [re.sub(r'\([^)]*\)', '', f).strip() for f in feedstocks]
            return [f for f in feedstocks if f and f.lower() not in ['various', 'see below', 'sources']]
        return []

    def _extract_yields(self, text: str, yield_patterns: List[str]) -> Dict[str, float]:
        """Extract yield data for specific gas types."""
        yields = {}
        
        for pattern in yield_patterns:
            section_match = re.search(f'- {re.escape(pattern)}:\\s*(.*?)(?=^- |$)', text, re.MULTILINE | re.DOTALL)
            if section_match:
                yield_section = section_match.group(1)
                
                # Extract individual yield entries
                yield_lines = [line.strip() for line in yield_section.split('\n') if line.strip() and line.strip().startswith('-')]
                
                for line in yield_lines:
                    # Parse patterns like "- Corncob: 61.2 mmol/g (Source: ...)"
                    yield_match = re.search(r'-\s*([^:]+):\s*([\d.]+)(?:\s*to\s*[\d.]+)?\s*([a-zA-Z₂/%.\s]+)', line)
                    if yield_match:
                        feedstock = yield_match.group(1).strip()
                        value = float(yield_match.group(2))  # Take first value for ranges
                        unit = yield_match.group(3).lower().replace('₂', '2').strip()
                        
                        # Convert to mol/kg
                        converted_value = self._convert_to_mol_kg(value, unit)
                        if converted_value is not None:
                            yields[feedstock] = converted_value
                    
                    # Also try parsing lines with percentage values like "55.84 vol.%"
                    elif 'vol.%' in line or '%' in line:
                        percent_match = re.search(r'-\s*([^:]+):\s*([\d.]+)\s*(?:vol\.)?%', line)
                        if percent_match:
                            feedstock = percent_match.group(1).strip()
                            # Store percentage values as negative to distinguish from mol/kg
                            yields[feedstock] = -float(percent_match.group(2))
                
                # Also check for single value entries
                single_match = re.search(r'([\d.]+)\s*([a-zA-Z₂/]+)', yield_section)
                if single_match and not yields:
                    value = float(single_match.group(1))
                    unit = single_match.group(2).lower().replace('₂', '2')
                    converted_value = self._convert_to_mol_kg(value, unit)
                    if converted_value is not None:
                        yields['general'] = converted_value
        
        return yields

    def _extract_conditions(self, text: str) -> Dict[str, Dict]:
        """Extract experimental conditions."""
        conditions = {}
        
        conditions_match = re.search(r'- Conditions:\s*(.*?)(?=^- |$)', text, re.MULTILINE | re.DOTALL)
        if conditions_match:
            conditions_text = conditions_match.group(1)
            
            # Parse individual condition lines
            condition_lines = [line.strip() for line in conditions_text.split('\n') if line.strip() and line.strip().startswith('-')]
            
            for line in condition_lines:
                # Extract feedstock name
                feedstock_match = re.search(r'-\s*([^:]+):', line)
                if feedstock_match:
                    feedstock = feedstock_match.group(1).strip()
                    
                    conditions[feedstock] = {}
                    
                    # Extract temperature
                    temp_match = re.search(r'(\d+(?:\.\d+)?)\s*[°◦]?\s*C', line, re.IGNORECASE)
                    if temp_match:
                        conditions[feedstock]['temperature_C'] = float(temp_match.group(1))
                    
                    # Extract pressure
                    pressure_match = re.search(r'(\d+(?:\.\d+)?)\s*(MPa|bar|atm)', line, re.IGNORECASE)
                    if pressure_match:
                        pressure_val = float(pressure_match.group(1))
                        pressure_unit = pressure_match.group(2).lower()
                        
                        # Convert to bar
                        if pressure_unit == 'mpa':
                            pressure_val *= 10
                        elif pressure_unit == 'atm':
                            pressure_val *= 1.01325
                        
                        conditions[feedstock]['pressure_bar'] = pressure_val
                    
                    # Extract time
                    time_match = re.search(r'(\d+)\s*min', line, re.IGNORECASE)
                    if time_match:
                        conditions[feedstock]['reaction_time_min'] = float(time_match.group(1))
        
        return conditions

    def _convert_to_mol_kg(self, value: float, unit: str) -> Optional[float]:
        """Convert various units to mol/kg."""
        unit = unit.lower().replace(' ', '').replace('₂', '2').replace('²', '2')
        
        # Handle volume percentages - return negative to flag as percentage
        if 'vol.%' in unit or 'vol%' in unit:
            return -value  # Negative indicates percentage
        elif '%' in unit and 'mol' not in unit:
            return -value  # Negative indicates percentage
        
        # Clean unit patterns
        unit = re.sub(r'[^\w/]', '', unit)  # Remove special characters
        
        if unit in self.unit_conversions:
            return value * self.unit_conversions[unit]
        elif unit.startswith('mol') and '/' not in unit:
            # Assume mol/kg when just "mol" variants
            return value * self.unit_conversions.get('mol', 1.0)
        elif unit.startswith('mmol') and '/' not in unit:
            # Assume mmol/kg when just "mmol" variants  
            return value * self.unit_conversions.get('mmol', 0.001)
        else:
            print(f"⚠️  Unknown unit: {unit}")
            return None

    def _standardize_feedstock(self, feedstock: str) -> str:
        """Standardize feedstock names."""
        feedstock_lower = feedstock.lower().strip()
        
        for key, value in self.feedstock_mapping.items():
            if key in feedstock_lower:
                return value
        
        # If no match found, clean up the name
        cleaned = re.sub(r'[^\w\s]', '', feedstock_lower)
        cleaned = re.sub(r'\s+', '_', cleaned.strip())
        return cleaned or 'unknown'
    
    def _format_yield_value(self, value) -> str:
        """Format yield values, handling both mol/kg and percentage values."""
        if value == '' or value is None:
            return ''
        
        if isinstance(value, (int, float)):
            if value < 0:
                # Negative values represent percentages
                return f"{abs(value):.2f}%"
            else:
                # Positive values are mol/kg
                return f"{value:.2f}"
        
        return str(value)

    def _create_entry_template(self, technology: str, filepath: str) -> Dict:
        """Create a template entry with default values."""
        filename = os.path.basename(filepath)
        study_ref = re.sub(r'_\d{8}_\d{6}\.md$', '', filename)
        
        return {
            'technology': technology,
            'temperature_C': '',
            'reaction_time_min': '',
            'pressure_bar': '',
            'feedstock_type': '',
            'agent_ratio': '',
            'H2_yield_mol_kg': '',
            'CO_yield_mol_kg': '',
            'CO2_yield_mol_kg': '',
            'CH4_yield_mol_kg': '',
            'carbon_efficiency_pct': '',
            'energy_input_kW': '',
            'reactor_type': '',
            'study_reference': study_ref,
            'notes': f'extracted_from_{filename}'
        }

    def process_all_files(self) -> pd.DataFrame:
        """Process all markdown files in the query results directory."""
        md_files = glob.glob(os.path.join(self.query_results_dir, "*.md"))
        
        if not md_files:
            print(f"❌ No markdown files found in {self.query_results_dir}")
            return pd.DataFrame()
        
        print(f"🔍 Processing {len(md_files)} query result files...")
        
        all_data = []
        for filepath in md_files:
            print(f"📄 Processing {os.path.basename(filepath)}")
            extracted = self.extract_from_markdown(filepath)
            all_data.extend(extracted)
        
        df = pd.DataFrame(all_data)
        
        print(f"✅ Extracted {len(df)} data entries")
        return df

    def save_to_csv(self, df: pd.DataFrame, output_file: str = None) -> str:
        """Save the extracted data to CSV."""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"extracted_gasification_data_{timestamp}.csv"
        
        # Ensure the DataFrame has the right column order
        expected_columns = [
            'technology', 'temperature_C', 'reaction_time_min', 'pressure_bar',
            'feedstock_type', 'agent_ratio', 'H2_yield_mol_kg', 'CO_yield_mol_kg',
            'CO2_yield_mol_kg', 'CH4_yield_mol_kg', 'carbon_efficiency_pct',
            'energy_input_kW', 'reactor_type', 'study_reference', 'notes'
        ]
        
        # Reorder columns and fill missing ones
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ''
        
        df = df[expected_columns]
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        print(f"📁 Data saved to: {output_file}")
        return output_file


def main():
    """Main function to run the extraction process."""
    print("🚀 Starting gasification data extraction from query results...")
    
    extractor = GasificationDataExtractor()
    df = extractor.process_all_files()
    
    if not df.empty:
        output_file = extractor.save_to_csv(df)
        
        # Print summary
        print(f"\n📊 EXTRACTION SUMMARY:")
        print(f"   Total entries: {len(df)}")
        print(f"   Technologies: {', '.join(df['technology'].unique())}")
        print(f"   Feedstocks: {len(df['feedstock_type'].unique())} unique types")
        print(f"   Output file: {output_file}")
        
        # Show preview
        print(f"\n📋 FIRST 3 ENTRIES:")
        print(df.head(3).to_string(index=False))
        
    else:
        print("❌ No data extracted. Check your query result files.")


if __name__ == "__main__":
    main() 