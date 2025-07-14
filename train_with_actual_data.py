#!/usr/bin/env python3
"""
Environmental Impact Prediction Using YOUR ACTUAL DATA
This script properly uses your gasification data and LCA results to train the model
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.inspection import permutation_importance
import warnings
warnings.filterwarnings('ignore')

def load_lca_results():
    """Load your actual LCA results from Excel file."""
    print("📊 Loading your actual LCA results from Excel file...")
    
    # Read the Excel file
    lca_df = pd.read_excel('data/LCA/LCAResultsWithWaste.xlsx')
    
    print(f"✅ LCA file loaded successfully!")
    print(f"📋 Shape: {lca_df.shape}")
    print(f"🔍 Columns: {list(lca_df.columns)}")
    
    return lca_df

def load_gasification_data():
    """Load your gasification experimental data."""
    print("\n🔬 Loading your gasification experimental data...")
    
    # Load operational gasification data
    gasification_df = pd.read_csv('data/gasification_data_refined.csv')
    
    print(f"✅ Gasification data loaded successfully!")
    print(f"📋 Shape: {gasification_df.shape}")
    print(f"🔍 Technologies: {gasification_df['technology'].unique()}")
    print(f"🔍 Feedstocks: {gasification_df['feedstock_type'].unique()}")
    
    return gasification_df

def process_lca_data(lca_df):
    """Process your LCA data into the format needed for modeling."""
    print("\n🔄 Processing LCA data structure...")
    
    # Clean column names
    lca_df.columns = [col.strip() for col in lca_df.columns]
    
    # Rename technology columns to match gasification data
    column_mapping = {
        'CO2 Gasfication': 'co2',
        'Plasma Gasification': 'plasma', 
        'SCWG': 'scw',
        'Steam Gasification': 'steam'
    }
    
    lca_df = lca_df.rename(columns=column_mapping)
    
    # Reshape from wide to long format
    impact_categories = lca_df['Impact categories'].tolist()
    
    # Create a list to hold the reshaped data
    reshaped_data = []
    
    for tech in ['co2', 'plasma', 'scw', 'steam']:
        tech_data = {'technology': tech}
        for i, category in enumerate(impact_categories):
            # Clean category name for column name
            clean_category = category.replace(' ', '_').replace('-', '_').lower()
            tech_data[clean_category] = lca_df[tech].iloc[i]
        reshaped_data.append(tech_data)
    
    # Create DataFrame
    impact_df = pd.DataFrame(reshaped_data)
    
    print(f"✅ LCA data processed successfully!")
    print(f"📊 Reshaped to: {impact_df.shape}")
    print(f"🔍 Impact categories: {len(impact_categories)}")
    print(f"🎯 Technologies: {impact_df['technology'].tolist()}")
    
    # Show the impact categories
    print(f"\n📋 Environmental Impact Categories:")
    for i, category in enumerate(impact_categories, 1):
        print(f"   {i:2d}. {category}")
    
    return impact_df, impact_categories

def merge_datasets(gasification_df, impact_df):
    """Merge gasification experimental data with LCA results."""
    print("\n🔗 Merging gasification data with LCA results...")
    
    # Merge on technology
    merged_df = pd.merge(gasification_df, impact_df, on='technology', how='left')
    
    # Fill missing values in operational parameters
    merged_df['agent_ratio'] = merged_df['agent_ratio'].fillna(merged_df['agent_ratio'].median())
    
    print(f"✅ Datasets merged successfully!")
    print(f"📊 Merged dataset shape: {merged_df.shape}")
    print(f"📋 Sample of merged data:")
    print(merged_df[['technology', 'temperature_C', 'feedstock_type', 'H2_yield_mol_kg']].head())
    
    return merged_df

def prepare_features_and_targets(merged_df, impact_categories):
    """Prepare features and targets for ML modeling."""
    print("\n🎯 Preparing features and targets...")
    
    # Input features (operational parameters)
    feature_columns = ['temperature_C', 'pressure_bar', 'agent_ratio', 'feedstock_type', 'technology']
    
    # Environmental impact targets (clean category names)
    impact_columns = []
    for category in impact_categories:
        clean_category = category.replace(' ', '_').replace('-', '_').lower()
        impact_columns.append(clean_category)
    
    # Encode categorical variables
    le_feedstock = LabelEncoder()
    le_technology = LabelEncoder()
    
    # Handle missing values in agent_ratio
    merged_df['agent_ratio'] = merged_df['agent_ratio'].fillna(1.0)
    
    merged_df['feedstock_encoded'] = le_feedstock.fit_transform(merged_df['feedstock_type'])
    merged_df['technology_encoded'] = le_technology.fit_transform(merged_df['technology'])
    
    # Feature matrix
    X = merged_df[['temperature_C', 'pressure_bar', 'agent_ratio', 'feedstock_encoded', 'technology_encoded']]
    
    # Target matrix (18 environmental impacts)
    y = merged_df[impact_columns]
    
    print(f"🔬 Features: {list(X.columns)}")
    print(f"🎯 Targets: {len(impact_columns)} environmental impact categories")
    print(f"📊 Dataset size: {X.shape[0]} samples")
    print(f"📋 Feedstock types: {list(le_feedstock.classes_)}")
    print(f"📋 Technologies: {list(le_technology.classes_)}")
    
    return X, y, impact_columns, le_feedstock, le_technology

def train_environmental_models(X, y, impact_columns):
    """Train multi-output models for environmental impact prediction."""
    print(f"\n🤖 Training Environmental Impact Models...")
    print("-" * 60)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data (using a larger test size due to small dataset)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    print(f"📊 Training set: {X_train.shape[0]} samples")
    print(f"📊 Test set: {X_test.shape[0]} samples")
    
    # Use simpler models for small dataset
    models = {
        'Random Forest': MultiOutputRegressor(
            RandomForestRegressor(n_estimators=50, max_depth=3, random_state=42)
        ),
        'Ridge Regression': MultiOutputRegressor(
            Ridge(alpha=1.0)
        )
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n🔧 Training {name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculate R² for each impact category
        r2_scores = []
        for i, category in enumerate(impact_columns):
            if len(y_test) > 0:
                r2 = r2_score(y_test.iloc[:, i], y_pred_test[:, i])
            else:
                r2 = 0.0
            r2_scores.append(r2)
        
        avg_r2 = np.mean(r2_scores)
        
        results[name] = {
            'model': model,
            'r2_scores': r2_scores,
            'avg_r2': avg_r2,
            'predictions_test': y_pred_test,
            'y_test': y_test
        }
        
        print(f"   Average R² = {avg_r2:.3f}")
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['avg_r2'])
    print(f"\n🏆 Best Model: {best_model_name} (R² = {results[best_model_name]['avg_r2']:.3f})")
    
    return results, best_model_name, scaler

def analyze_results(results, best_model_name, impact_columns, impact_categories):
    """Analyze model performance and create visualizations."""
    print(f"\n📊 Analyzing {best_model_name} Performance...")
    print("-" * 60)
    
    best_result = results[best_model_name]
    r2_scores = best_result['r2_scores']
    
    # Create performance DataFrame
    performance_df = pd.DataFrame({
        'Impact_Category': impact_categories,
        'Clean_Name': impact_columns,
        'R2_Score': r2_scores
    }).sort_values('R2_Score', ascending=False)
    
    print(f"📈 Top 10 Best Predicted Categories:")
    for _, row in performance_df.head(10).iterrows():
        print(f"   {row['Impact_Category'][:40]:40s}: R² = {row['R2_Score']:.3f}")
    
    print(f"\n📉 Most Challenging Categories:")
    for _, row in performance_df.tail(5).iterrows():
        print(f"   {row['Impact_Category'][:40]:40s}: R² = {row['R2_Score']:.3f}")
    
    return performance_df

def create_technology_comparison(impact_df, impact_categories):
    """Create technology comparison using your actual LCA data."""
    print(f"\n🌍 Environmental Impact Comparison (Your Actual Data):")
    print("-" * 60)
    
    # Calculate overall environmental score (normalized)
    impact_columns = [col for col in impact_df.columns if col != 'technology']
    
    # Normalize each impact category (0-1 scale)
    normalized_impacts = impact_df.copy()
    for col in impact_columns:
        col_min = impact_df[col].min()
        col_max = impact_df[col].max()
        if col_max != col_min:
            normalized_impacts[col] = (impact_df[col] - col_min) / (col_max - col_min)
        else:
            normalized_impacts[col] = 0.0
    
    # Overall score (lower is better)
    normalized_impacts['overall_score'] = normalized_impacts[impact_columns].mean(axis=1)
    
    # Ranking
    ranking = normalized_impacts[['technology', 'overall_score']].sort_values('overall_score')
    
    print(f"🏆 Technology Ranking (Lower Score = Better):")
    for i, (_, row) in enumerate(ranking.iterrows(), 1):
        print(f"   {i}. {row['technology'].upper():10s}: {row['overall_score']:.3f}")
    
    return ranking

def create_prediction_function(model, scaler, impact_columns, le_feedstock, le_technology, impact_categories):
    """Create function to predict environmental impacts for new conditions."""
    
    def predict_impacts(temperature, pressure, agent_ratio, feedstock, technology):
        """Predict environmental impacts for given gasification conditions."""
        
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
    
    return predict_impacts

def main():
    """Main function to train model with your actual data."""
    print("🌍 Training Environmental Impact Model with YOUR ACTUAL DATA")
    print("=" * 70)
    
    # Load your actual data
    lca_df = load_lca_results()
    gasification_df = load_gasification_data()
    
    # Process LCA data
    impact_df, impact_categories = process_lca_data(lca_df)
    
    # Merge datasets
    merged_df = merge_datasets(gasification_df, impact_df)
    
    # Prepare features and targets
    X, y, impact_columns, le_feedstock, le_technology = prepare_features_and_targets(merged_df, impact_categories)
    
    # Train models
    results, best_model_name, scaler = train_environmental_models(X, y, impact_columns)
    
    # Analyze results
    performance_df = analyze_results(results, best_model_name, impact_columns, impact_categories)
    
    # Technology comparison
    ranking = create_technology_comparison(impact_df, impact_categories)
    
    # Create prediction function
    best_model = results[best_model_name]['model']
    predict_function = create_prediction_function(
        best_model, scaler, impact_columns, le_feedstock, le_technology, impact_categories
    )
    
    print(f"\n✨ Model Training Complete!")
    print(f"🏆 Best model: {best_model_name}")
    print(f"📊 Trained on {X.shape[0]} experimental data points")
    print(f"🎯 Predicts {len(impact_categories)} environmental impact categories")
    
    # Example prediction
    print(f"\n🔮 Example Prediction:")
    print(f"   Conditions: 750°C, 10 bar, steam ratio 1.0, bagasse, steam gasification")
    example_pred = predict_function(750, 10, 1.0, 'bagasse', 'steam')
    if example_pred is not None:
        print(f"   Top 5 predicted impacts:")
        for _, row in example_pred.head().iterrows():
            print(f"      {row['Impact_Category'][:35]:35s}: {row['Predicted_Value']:.6f}")
    
    return results, performance_df, ranking, predict_function

if __name__ == "__main__":
    results, performance_df, ranking, predict_function = main() 