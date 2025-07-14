#!/usr/bin/env python3
"""
Environmental Impact Prediction for Gasification Technologies
Multi-output ML model to predict 18 LCA impact categories
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

def create_environmental_impact_data():
    """Create the environmental impact dataset from your LCA results."""
    
    # Environmental impact data from your table
    impact_data = {
        'technology': ['co2', 'plasma', 'scw', 'steam'],
        'agricultural_land_occupation': [0.00021, 0.00016, 0.00015, 0.00017],
        'climate_change': [1.83297, 0.89236, 0.58298, 1.49028],
        'fossil_depletion': [0.45623, 0.2606, 0.17269, 0.46359],
        'freshwater_ecotoxicity': [0.05756, 0.01416, 0.01275, 0.06116],
        'freshwater_eutrophication': [0.00091, 0.0006, 0.00046, 0.00098],
        'human_toxicity': [0.71295, 0.41587, 0.30768, 0.68349],
        'ionising_radiation': [0.38193, 0.21775, 0.18718, 0.3971],
        'marine_ecotoxicity': [0.05075, 0.0123, 0.01094, 0.05277],
        'marine_eutrophication': [0.00132, 0.00077, 0.00046, 0.001],
        'metal_depletion': [0.00134, 0.00071, 0.00062, 0.0013],
        'natural_land_transformation': [4.30E-05, 1.96E-05, 1.08E-05, 2.45E-05],
        'ozone_depletion': [9.88E-08, 3.80E-08, 3.10E-08, 9.73E-08],
        'particulate_matter_formation': [0.00281, 0.00256, 0.00172, 0.00372],
        'photochemical_oxidant_formation': [0.00323, 0.00208, 0.00123, 0.00268],
        'terrestrial_acidification': [0.0043, 0.00282, 0.0016, 0.00398],
        'terrestrial_ecotoxicity': [0.00046, 7.35E-05, 7.40E-05, 0.00015],
        'urban_land_occupation': [0.00931, 0.00621, 0.00412, 0.00765],
        'water_depletion': [0.01146, 0.00429, 0.00348, 0.00671]
    }
    
    impact_df = pd.DataFrame(impact_data)
    print(f"📊 Environmental impact data created: {len(impact_df)} technologies, {len(impact_df.columns)-1} impact categories")
    
    return impact_df

def load_and_merge_datasets():
    """Load gasification data and merge with environmental impacts."""
    
    # Load operational gasification data
    gasification_df = pd.read_csv('data/gasification_data_refined.csv')
    
    # Rename columns for consistency
    gasification_df = gasification_df.rename(columns={
        'temperature_C': 'temperature',
        'reaction_time_min': 'reaction_time',
        'pressure_bar': 'pressure',
        'agent_ratio': 'steam_ratio',
        'feedstock_type': 'feedstock',
        'technology': 'technology',
        'H2_yield_mol_kg': 'H2_yield',
        'CO_yield_mol_kg': 'CO_yield'
    })
    
    # Load environmental impact data
    impact_df = create_environmental_impact_data()
    
    # Merge datasets on technology
    merged_df = pd.merge(gasification_df, impact_df, on='technology', how='left')
    
    # Fill missing values
    merged_df['steam_ratio'] = merged_df['steam_ratio'].fillna(merged_df['steam_ratio'].median())
    
    print(f"✅ Merged dataset: {len(merged_df)} entries with operational and environmental data")
    
    return merged_df, impact_df

def prepare_features_and_targets(df):
    """Prepare features and targets for ML modeling."""
    
    # Input features (operational parameters)
    feature_columns = ['temperature', 'pressure', 'steam_ratio', 'feedstock', 'technology']
    
    # Environmental impact targets (18 categories)
    impact_columns = [
        'agricultural_land_occupation', 'climate_change', 'fossil_depletion',
        'freshwater_ecotoxicity', 'freshwater_eutrophication', 'human_toxicity',
        'ionising_radiation', 'marine_ecotoxicity', 'marine_eutrophication',
        'metal_depletion', 'natural_land_transformation', 'ozone_depletion',
        'particulate_matter_formation', 'photochemical_oxidant_formation',
        'terrestrial_acidification', 'terrestrial_ecotoxicity',
        'urban_land_occupation', 'water_depletion'
    ]
    
    # Encode categorical variables
    le_feedstock = LabelEncoder()
    le_technology = LabelEncoder()
    
    df['feedstock_encoded'] = le_feedstock.fit_transform(df['feedstock'])
    df['technology_encoded'] = le_technology.fit_transform(df['technology'])
    
    # Feature matrix
    X = df[['temperature', 'pressure', 'steam_ratio', 'feedstock_encoded', 'technology_encoded']]
    
    # Target matrix (18 environmental impacts)
    y = df[impact_columns]
    
    print(f"🔬 Features: {list(X.columns)}")
    print(f"🎯 Targets: {len(impact_columns)} environmental impact categories")
    
    return X, y, impact_columns, le_feedstock, le_technology

def train_environmental_models(X, y, impact_columns):
    """Train multi-output models for environmental impact prediction."""
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
    
    models = {
        'Random Forest': MultiOutputRegressor(
            RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
        ),
        'Ridge Regression': MultiOutputRegressor(
            Ridge(alpha=1.0)
        ),
        'Neural Network': MultiOutputRegressor(
            MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
        )
    }
    
    results = {}
    
    print("\n🤖 Training Environmental Impact Models:")
    print("-" * 50)
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculate R² for each impact category
        r2_scores = []
        for i, category in enumerate(impact_columns):
            r2 = r2_score(y_test.iloc[:, i], y_pred_test[:, i])
            r2_scores.append(r2)
        
        avg_r2 = np.mean(r2_scores)
        
        results[name] = {
            'model': model,
            'r2_scores': r2_scores,
            'avg_r2': avg_r2,
            'predictions_test': y_pred_test,
            'y_test': y_test
        }
        
        print(f"{name:20s}: Average R² = {avg_r2:.3f}")
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['avg_r2'])
    print(f"\n🏆 Best Model: {best_model_name} (R² = {results[best_model_name]['avg_r2']:.3f})")
    
    return results, best_model_name, scaler, X_test, y_test

def analyze_impact_predictions(results, best_model_name, impact_columns):
    """Analyze model performance for each environmental impact category."""
    
    best_result = results[best_model_name]
    r2_scores = best_result['r2_scores']
    
    # Create performance DataFrame
    performance_df = pd.DataFrame({
        'Impact_Category': impact_columns,
        'R2_Score': r2_scores
    }).sort_values('R2_Score', ascending=False)
    
    print(f"\n📊 {best_model_name} Performance by Impact Category:")
    print("-" * 60)
    for _, row in performance_df.head(10).iterrows():
        print(f"{row['Impact_Category']:35s}: R² = {row['R2_Score']:.3f}")
    
    # Plot performance
    plt.figure(figsize=(14, 8))
    
    plt.subplot(2, 2, 1)
    sns.barplot(data=performance_df.head(10), x='R2_Score', y='Impact_Category', palette='viridis')
    plt.title('Top 10 Best Predicted Impact Categories')
    plt.xlabel('R² Score')
    
    plt.subplot(2, 2, 2)
    sns.barplot(data=performance_df.tail(8), x='R2_Score', y='Impact_Category', palette='plasma')
    plt.title('Most Challenging Impact Categories')
    plt.xlabel('R² Score')
    
    # Actual vs Predicted for best categories
    y_test = best_result['y_test']
    y_pred = best_result['predictions_test']
    
    # Best predicted category
    best_idx = performance_df.index[0]
    best_category = performance_df.iloc[0]['Impact_Category']
    
    plt.subplot(2, 2, 3)
    plt.scatter(y_test.iloc[:, best_idx], y_pred[:, best_idx], alpha=0.7)
    plt.plot([y_test.iloc[:, best_idx].min(), y_test.iloc[:, best_idx].max()], 
             [y_test.iloc[:, best_idx].min(), y_test.iloc[:, best_idx].max()], 'r--')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title(f'Best: {best_category}')
    
    # Most challenging category
    worst_idx = performance_df.index[-1]
    worst_category = performance_df.iloc[-1]['Impact_Category']
    
    plt.subplot(2, 2, 4)
    plt.scatter(y_test.iloc[:, worst_idx], y_pred[:, worst_idx], alpha=0.7, color='red')
    plt.plot([y_test.iloc[:, worst_idx].min(), y_test.iloc[:, worst_idx].max()], 
             [y_test.iloc[:, worst_idx].min(), y_test.iloc[:, worst_idx].max()], 'r--')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title(f'Challenging: {worst_category}')
    
    plt.tight_layout()
    plt.show()
    
    return performance_df

def create_technology_comparison(impact_df):
    """Create comprehensive technology comparison across all impact categories."""
    
    # Normalize impacts for comparison (0-1 scale for each category)
    impact_normalized = impact_df.copy()
    impact_columns = impact_df.columns[1:]  # Exclude 'technology'
    
    for col in impact_columns:
        impact_normalized[col] = (impact_df[col] - impact_df[col].min()) / (impact_df[col].max() - impact_df[col].min())
    
    # Calculate overall environmental score (lower is better)
    impact_normalized['overall_score'] = impact_normalized[impact_columns].mean(axis=1)
    
    print("\n🌍 Environmental Impact Ranking (Lower is Better):")
    print("-" * 50)
    ranking = impact_normalized[['technology', 'overall_score']].sort_values('overall_score')
    for _, row in ranking.iterrows():
        print(f"{row['technology'].upper():15s}: {row['overall_score']:.3f}")
    
    # Create heatmap
    plt.figure(figsize=(16, 10))
    
    # Prepare data for heatmap
    heatmap_data = impact_df.set_index('technology')[impact_columns].T
    
    sns.heatmap(heatmap_data, annot=True, fmt='.4f', cmap='RdYlBu_r', center=0.5)
    plt.title('Environmental Impact Heatmap by Technology\n(Red = Higher Impact, Blue = Lower Impact)')
    plt.xlabel('Gasification Technology')
    plt.ylabel('Environmental Impact Category')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()
    
    return ranking, impact_normalized

def predict_new_conditions(model, scaler, impact_columns, le_feedstock, le_technology):
    """Function to predict environmental impacts for new operating conditions."""
    
    def make_prediction(temperature, pressure, steam_ratio, feedstock, technology):
        """Make environmental impact prediction for given conditions."""
        
        # Encode categorical variables
        try:
            feedstock_encoded = le_feedstock.transform([feedstock])[0]
            technology_encoded = le_technology.transform([technology])[0]
        except ValueError as e:
            print(f"Error: Unknown feedstock or technology. Available options:")
            print(f"Feedstocks: {list(le_feedstock.classes_)}")
            print(f"Technologies: {list(le_technology.classes_)}")
            return None
        
        # Prepare input
        X_new = np.array([[temperature, pressure, steam_ratio, feedstock_encoded, technology_encoded]])
        X_new_scaled = scaler.transform(X_new)
        
        # Predict
        prediction = model.predict(X_new_scaled)[0]
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'Impact_Category': impact_columns,
            'Predicted_Value': prediction
        })
        
        return results_df
    
    return make_prediction

def main():
    """Main function for environmental impact ML analysis."""
    print("🌍 Environmental Impact Prediction for Gasification Technologies")
    print("=" * 70)
    
    # Load and merge datasets
    print("\n1. Loading and merging datasets...")
    merged_df, impact_df = load_and_merge_datasets()
    
    # Prepare features and targets
    print("\n2. Preparing features and targets...")
    X, y, impact_columns, le_feedstock, le_technology = prepare_features_and_targets(merged_df)
    
    # Train models
    print("\n3. Training environmental impact models...")
    results, best_model_name, scaler, X_test, y_test = train_environmental_models(X, y, impact_columns)
    
    # Analyze predictions
    print("\n4. Analyzing impact predictions...")
    performance_df = analyze_impact_predictions(results, best_model_name, impact_columns)
    
    # Technology comparison
    print("\n5. Creating technology comparison...")
    ranking, impact_normalized = create_technology_comparison(impact_df)
    
    # Create prediction function
    best_model = results[best_model_name]['model']
    predict_function = predict_new_conditions(best_model, scaler, impact_columns, le_feedstock, le_technology)
    
    print(f"\n✨ Analysis complete!")
    print(f"🏆 Best model: {best_model_name}")
    print(f"🎯 Can now predict environmental impacts for new gasification conditions")
    
    # Example prediction
    print(f"\n🔮 Example prediction for 750°C, 10 bar, steam ratio 1.0, bagasse, steam:")
    example_pred = predict_function(750, 10, 1.0, 'bagasse', 'steam')
    if example_pred is not None:
        print(example_pred.head())
    
    return results, performance_df, ranking, predict_function

if __name__ == "__main__":
    results, performance_df, ranking, predict_function = main() 