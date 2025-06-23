import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import os

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class LCAResultsVisualizer:
    def __init__(self, excel_file_path):
        """Initialize the visualizer with Excel data"""
        self.excel_path = excel_file_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Load and clean the Excel data"""
        try:
            self.df = pd.read_excel(self.excel_path)
            print(f"✅ Loaded data with shape: {self.df.shape}")
            print(f"📊 Impact categories: {len(self.df)}")
            print(f"🔬 Technologies: {len(self.df.columns) - 2}")  # Excluding 'Impact categories' and 'Unit'
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return
            
        # Clean column names
        self.df.columns = self.df.columns.str.strip()
        
        # Get technology columns (excluding Impact categories and Unit)
        self.tech_columns = [col for col in self.df.columns if col not in ['Impact categories', 'Unit']]
        print(f"🏭 Technologies found: {self.tech_columns}")
        
    def create_single_pie_chart(self, impact_category, save_path=None, show_plot=True):
        """Create a pie chart for a single impact category"""
        
        # Get the row for this impact category
        row = self.df[self.df['Impact categories'] == impact_category]
        
        if row.empty:
            print(f"❌ Impact category '{impact_category}' not found")
            return
            
        # Extract values and unit
        values = row[self.tech_columns].values[0]
        unit = row['Unit'].values[0]
        
        # Filter out zero or negative values
        tech_names = []
        tech_values = []
        for i, val in enumerate(values):
            if val > 0:  # Only include positive values
                tech_names.append(self.tech_columns[i])
                tech_values.append(val)
        
        if len(tech_values) == 0:
            print(f"⚠️ No positive values found for '{impact_category}'")
            return
            
        # Create the pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Generate colors
        colors = sns.color_palette("husl", len(tech_values))
        
        # Create pie chart with enhanced styling
        wedges, texts, autotexts = ax.pie(
            tech_values, 
            labels=tech_names,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.05] * len(tech_values),  # Slightly separate all wedges
            shadow=True,
            textprops={'fontsize': 10, 'weight': 'bold'}
        )
        
        # Enhance the appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
            
        # Set title
        ax.set_title(f'{impact_category}\n({unit})', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Add value labels outside the pie
        for i, (wedge, value, name) in enumerate(zip(wedges, tech_values, tech_names)):
            angle = (wedge.theta2 + wedge.theta1) / 2
            x = 1.3 * np.cos(np.radians(angle))
            y = 1.3 * np.sin(np.radians(angle))
            ax.annotate(f'{name}\n{value:.4f} {unit}', 
                       xy=(x, y), ha='center', va='center',
                       fontsize=9, weight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[i], alpha=0.3))
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Saved: {save_path}")
            
        if show_plot:
            plt.show()
        else:
            plt.close()
            
    def create_all_pie_charts(self, output_dir="plots/pie_charts", show_plots=False):
        """Create pie charts for all impact categories"""
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print(f"\n🎯 Creating pie charts for {len(self.df)} impact categories...")
        print(f"📁 Output directory: {output_dir}")
        
        for index, row in self.df.iterrows():
            impact_category = row['Impact categories']
            
            # Clean filename
            clean_name = "".join(c for c in impact_category if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{clean_name.replace(' ', '_')}.png"
            save_path = os.path.join(output_dir, filename)
            
            print(f"\n📊 Creating chart {index+1}/{len(self.df)}: {impact_category}")
            
            self.create_single_pie_chart(
                impact_category=impact_category,
                save_path=save_path,
                show_plot=show_plots
            )
            
        print(f"\n✅ All charts created successfully!")
        print(f"📂 Check the '{output_dir}' directory for your pie charts")
        
    def create_summary_comparison(self, output_dir="plots", show_plot=True):
        """Create a summary comparison showing relative performance across all categories"""
        
        # Calculate total impact for each technology (normalized)
        tech_totals = {}
        
        for tech in self.tech_columns:
            # Normalize each impact category to 0-1 scale, then sum
            normalized_sum = 0
            valid_categories = 0
            
            for _, row in self.df.iterrows():
                values = self.df[self.tech_columns].loc[self.df.index == row.name].values[0]
                max_val = max(values)
                
                if max_val > 0:  # Avoid division by zero
                    normalized_val = row[tech] / max_val
                    normalized_sum += normalized_val
                    valid_categories += 1
                    
            tech_totals[tech] = normalized_sum / valid_categories if valid_categories > 0 else 0
        
        # Create summary pie chart
        fig, ax = plt.subplots(figsize=(12, 8))
        
        techs = list(tech_totals.keys())
        values = list(tech_totals.values())
        colors = sns.color_palette("husl", len(techs))
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=techs,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.1] * len(values),
            shadow=True,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
            autotext.set_fontsize(12)
            
        ax.set_title('Overall Environmental Impact Comparison\n(Lower is Better)', 
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        save_path = os.path.join(output_dir, "overall_comparison.png")
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Saved summary chart: {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
            
    def print_data_summary(self):
        """Print a summary of the data"""
        print("\n" + "="*80)
        print("📋 LCA RESULTS DATA SUMMARY")
        print("="*80)
        
        print(f"📊 Total Impact Categories: {len(self.df)}")
        print(f"🏭 Technologies Compared: {len(self.tech_columns)}")
        print(f"📁 Source File: {self.excel_path}")
        
        print(f"\n🔬 Technologies:")
        for i, tech in enumerate(self.tech_columns, 1):
            print(f"  {i}. {tech}")
            
        print(f"\n🌍 Impact Categories:")
        for i, category in enumerate(self.df['Impact categories'], 1):
            unit = self.df[self.df['Impact categories'] == category]['Unit'].values[0]
            print(f"  {i:2d}. {category} ({unit})")
        
        print("="*80)

def main():
    """Main function to run the LCA visualization"""
    
    # File path - handle both running from root directory and plot directory
    excel_file = "../data/LCA/LCAResultsWithWaste.xlsx"
    if not os.path.exists(excel_file):
        excel_file = "data/LCA/LCAResultsWithWaste.xlsx"  # If running from root
    
    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    # Create visualizer
    visualizer = LCAResultsVisualizer(excel_file)
    
    # Print data summary
    visualizer.print_data_summary()
    
    # Ask user what they want to do
    print(f"\n🎯 What would you like to create?")
    print(f"1. All pie charts (saved to files)")
    print(f"2. Single pie chart (interactive)")
    print(f"3. Overall comparison summary")
    print(f"4. All of the above")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        visualizer.create_all_pie_charts(show_plots=False)
        
    elif choice == "2":
        print(f"\nAvailable impact categories:")
        for i, category in enumerate(visualizer.df['Impact categories'], 1):
            print(f"  {i}. {category}")
        
        try:
            idx = int(input(f"\nEnter category number (1-{len(visualizer.df)}): ")) - 1
            category = visualizer.df['Impact categories'].iloc[idx]
            visualizer.create_single_pie_chart(category)
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            
    elif choice == "3":
        visualizer.create_summary_comparison()
        
    elif choice == "4":
        visualizer.create_all_pie_charts(show_plots=False)
        visualizer.create_summary_comparison(show_plot=False)
        print("\n✅ All visualizations created!")
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
