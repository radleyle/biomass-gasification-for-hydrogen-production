#!/usr/bin/env python3
"""
Environmental Impact Predictor - Trained on YOUR Data
Use this script to predict environmental impacts for any gasification conditions
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load and prepare data (same as training)
def load_and_prepare_data():
    """Load your data and prepare encoders - same as training."""
    
    # Load LCA results
    lca_df = pd.read_excel('data/LCA/LCAResultsWithWaste.xlsx')
    lca_df.columns = [col.strip() for col in lca_df.columns]
    
    column_mapping = {
        'CO2 Gasfication': 'co2',
        'Plasma Gasification': 'plasma', 
        'SCWG': 'scw',
        'Steam Gasification': 'steam'
    }
    lca_df = lca_df.rename(columns=column_mapping)
    
    # Load gasification data
    gasification_df = pd.read_csv('data/gasification_data_refined.csv')
    
    # Process LCA data
    impact_categories = lca_df['Impact categories'].tolist()
    reshaped_data = []
    
    for tech in ['co2', 'plasma', 'scw', 'steam']:
        tech_data = {'technology': tech}
        for i, category in enumerate(impact_categories):
            clean_category = category.replace(' ', '_').replace('-', '_').lower()
            tech_data[clean_category] = lca_df[tech].iloc[i]
        reshaped_data.append(tech_data)
    
    impact_df = pd.DataFrame(reshaped_data)
    
    # Merge datasets
    merged_df = pd.merge(gasification_df, impact_df, on='technology', how='left')
    merged_df['agent_ratio'] = merged_df['agent_ratio'].fillna(1.0)
    
    # Prepare encoders
    le_feedstock = LabelEncoder()
    le_technology = LabelEncoder()
    
    le_feedstock.fit(merged_df['feedstock_type'])
    le_technology.fit(merged_df['technology'])
    
    # Prepare features and targets
    merged_df['feedstock_encoded'] = le_feedstock.transform(merged_df['feedstock_type'])
    merged_df['technology_encoded'] = le_technology.transform(merged_df['technology'])
    
    X = merged_df[['temperature_C', 'pressure_bar', 'agent_ratio', 'feedstock_encoded', 'technology_encoded']]
    
    impact_columns = []
    for category in impact_categories:
        clean_category = category.replace(' ', '_').replace('-', '_').lower()
        impact_columns.append(clean_category)
    
    y = merged_df[impact_columns]
    
    return X, y, impact_categories, le_feedstock, le_technology

# Train and save model
def train_and_save_model():
    """Train the model with your data and save it."""
    print("🔧 Training model with your actual data...")
    
    X, y, impact_categories, le_feedstock, le_technology = load_and_prepare_data()
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=50, max_depth=3, random_state=42))
    model.fit(X_scaled, y)
    
    # Save model and encoders
    joblib.dump(model, 'environmental_impact_model.pkl')
    joblib.dump(scaler, 'feature_scaler.pkl')
    joblib.dump(le_feedstock, 'feedstock_encoder.pkl')
    joblib.dump(le_technology, 'technology_encoder.pkl')
    joblib.dump(impact_categories, 'impact_categories.pkl')
    
    print("✅ Model trained and saved successfully!")
    return model, scaler, le_feedstock, le_technology, impact_categories

# Load model
def load_model():
    """Load the trained model."""
    try:
        model = joblib.load('environmental_impact_model.pkl')
        scaler = joblib.load('feature_scaler.pkl')
        le_feedstock = joblib.load('feedstock_encoder.pkl')
        le_technology = joblib.load('technology_encoder.pkl')
        impact_categories = joblib.load('impact_categories.pkl')
        return model, scaler, le_feedstock, le_technology, impact_categories
    except FileNotFoundError:
        print("⚠️ Model not found. Training new model...")
        return train_and_save_model()

# Prediction function
def predict_environmental_impact(temperature, pressure, agent_ratio, feedstock, technology):
    """
    Predict environmental impacts for given gasification conditions.
    
    Parameters:
    - temperature: Temperature in °C (e.g., 750)
    - pressure: Pressure in bar (e.g., 10)
    - agent_ratio: Agent ratio (e.g., 1.0)
    - feedstock: Feedstock type (e.g., 'bagasse', 'biomass', 'wood_chips')
    - technology: Technology type ('co2', 'steam', 'scw', 'plasma')
    
    Returns:
    - DataFrame with predicted environmental impacts
    """
    
    # Load model
    model, scaler, le_feedstock, le_technology, impact_categories = load_model()
    
    try:
        # Encode categorical variables
        feedstock_encoded = le_feedstock.transform([feedstock])[0]
        technology_encoded = le_technology.transform([technology])[0]
        
        # Prepare input
        X_new = np.array([[temperature, pressure, agent_ratio, feedstock_encoded, technology_encoded]])
        X_new_scaled = scaler.transform(X_new)
        
        # Predict
        prediction = model.predict(X_new_scaled)[0]
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'Impact_Category': impact_categories,
            'Predicted_Value': prediction
        })
        
        return results_df
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print(f"📋 Available feedstocks: {list(le_feedstock.classes_)}")
        print(f"📋 Available technologies: {list(le_technology.classes_)}")
        return None

# Technology comparison
def compare_technologies():
    """Compare environmental performance of different technologies."""
    
    print("\n🌍 Technology Comparison (Based on Your LCA Data):")
    print("-" * 60)
    
    # Load your actual LCA results
    lca_df = pd.read_excel('data/LCA/LCAResultsWithWaste.xlsx')
    lca_df.columns = [col.strip() for col in lca_df.columns]
    
    column_mapping = {
        'CO2 Gasfication': 'co2',
        'Plasma Gasification': 'plasma', 
        'SCWG': 'scw',
        'Steam Gasification': 'steam'
    }
    lca_df = lca_df.rename(columns=column_mapping)
    
    # Show climate change impact (most important)
    climate_row = lca_df[lca_df['Impact categories'] == 'climate change']
    if not climate_row.empty:
        print("📊 Climate Change Impact (kg CO2-Eq):")
        climate_data = [(tech, climate_row[tech].values[0]) for tech in ['co2', 'plasma', 'scw', 'steam']]
        climate_data.sort(key=lambda x: x[1])
        
        for i, (tech, impact) in enumerate(climate_data, 1):
            print(f"   {i}. {tech.upper():8s}: {impact:.3f} kg CO2-Eq")
    
    # Overall ranking
    print(f"\n🏆 Overall Environmental Ranking (Lower = Better):")
    print(f"   1. SCW (Supercritical Water)")
    print(f"   2. Plasma")
    print(f"   3. CO2")
    print(f"   4. Steam")

# Main interactive function
def main():
    """Interactive prediction interface."""
    print("🌍 Environmental Impact Predictor")
    print("=" * 50)
    print("Trained on your actual gasification data and LCA results!")
    
    # Show available options
    _, _, le_feedstock, le_technology, _ = load_model()
    
    print(f"\n📋 Available Options:")
    print(f"Technologies: {list(le_technology.classes_)}")
    print(f"Feedstocks: {list(le_feedstock.classes_)}")
    
    # Technology comparison
    compare_technologies()
    
    # Example predictions
    print(f"\n🔮 Example Predictions:")
    print("-" * 30)
    
    examples = [
        (800, 1, 1.0, 'rice_husk', 'co2'),
        (750, 10, 1.0, 'bagasse', 'steam'),
        (600, 250, 1.0, 'food_waste', 'scw'),
        (1200, 1, 1.0, 'wood_pellets', 'plasma')
    ]
    
    for temp, press, ratio, feedstock, tech in examples:
        print(f"\n🔬 {tech.upper()} gasification of {feedstock} at {temp}°C:")
        result = predict_environmental_impact(temp, press, ratio, feedstock, tech)
        if result is not None:
            # Show top 5 impacts
            for _, row in result.head(5).iterrows():
                print(f"   {row['Impact_Category'][:30]:30s}: {row['Predicted_Value']:.6f}")
    
    print(f"\n✨ Use predict_environmental_impact() function for custom predictions!")

if __name__ == "__main__":
    main() 