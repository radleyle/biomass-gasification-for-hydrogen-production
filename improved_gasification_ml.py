#!/usr/bin/env python3
"""
Improved Gasification ML Model
Better approaches for small experimental datasets
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error
import seaborn as sns

def load_and_prepare_data():
    """Load and prepare gasification data with smart preprocessing."""
    df = pd.read_csv('data/gasification_data_refined.csv')
    
    # Focus on key features for small dataset
    df_ml = df.rename(columns={
        'temperature_C': 'temperature',
        'pressure_bar': 'pressure',
        'technology': 'gasifier_type',
        'feedstock_type': 'feedstock',
        'H2_yield_mol_kg': 'H2_yield'
    })
    
    # Simple feature engineering
    features = ['temperature', 'pressure', 'gasifier_type', 'feedstock']
    
    # Encode categorical variables numerically (more efficient for small data)
    le_gasifier = LabelEncoder()
    le_feedstock = LabelEncoder()
    
    df_ml['gasifier_encoded'] = le_gasifier.fit_transform(df_ml['gasifier_type'])
    df_ml['feedstock_encoded'] = le_feedstock.fit_transform(df_ml['feedstock'])
    
    # Final feature set
    X = df_ml[['temperature', 'pressure', 'gasifier_encoded', 'feedstock_encoded']]
    y = df_ml['H2_yield']
    
    print(f"📊 Dataset: {len(df_ml)} samples, {len(X.columns)} features")
    print(f"🔬 Features: {list(X.columns)}")
    print(f"📈 H2 yield range: {y.min():.2f} - {y.max():.2f} mol/kg")
    
    return X, y, le_gasifier, le_feedstock, df_ml

def compare_models(X, y):
    """Compare different ML models using cross-validation."""
    
    # Scale features for linear models
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Random Forest': RandomForestRegressor(n_estimators=50, max_depth=3, random_state=42),
    }
    
    results = {}
    
    print("\n🔍 Model Comparison (Cross-Validation):")
    print("-" * 50)
    
    for name, model in models.items():
        if 'Linear' in name or 'Ridge' in name:
            X_input = X_scaled
        else:
            X_input = X
            
        # Use Leave-One-Out CV for small dataset
        cv_scores = cross_val_score(model, X_input, y, cv=LeaveOneOut(), 
                                   scoring='r2', n_jobs=-1)
        
        mean_score = cv_scores.mean()
        std_score = cv_scores.std()
        
        results[name] = {
            'model': model,
            'X_input': X_input,
            'cv_scores': cv_scores,
            'mean_r2': mean_score,
            'std_r2': std_score
        }
        
        print(f"{name:20s}: R² = {mean_score:.3f} ± {std_score:.3f}")
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['mean_r2'])
    best_result = results[best_model_name]
    
    print(f"\n🏆 Best Model: {best_model_name} (R² = {best_result['mean_r2']:.3f})")
    
    return results, best_model_name

def analyze_feature_importance(X, y):
    """Analyze which features are most important."""
    
    # Train Random Forest for feature importance
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n🔍 Feature Importance Analysis:")
    print("-" * 30)
    for _, row in feature_importance.iterrows():
        print(f"{row['feature']:20s}: {row['importance']:.3f}")
    
    # Plot feature importance
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance, x='importance', y='feature', palette='viridis')
    plt.title('Feature Importance for H2 Yield Prediction')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()
    
    return feature_importance

def create_technology_analysis(df_ml):
    """Analyze H2 yield by gasification technology."""
    
    plt.figure(figsize=(12, 8))
    
    # Technology comparison
    plt.subplot(2, 2, 1)
    tech_summary = df_ml.groupby('gasifier_type')['H2_yield'].agg(['mean', 'std', 'count'])
    tech_summary['mean'].plot(kind='bar', color='skyblue', alpha=0.7)
    plt.title('Average H2 Yield by Technology')
    plt.ylabel('H2 Yield (mol/kg)')
    plt.xticks(rotation=45)
    
    # Feedstock comparison
    plt.subplot(2, 2, 2)
    feedstock_summary = df_ml.groupby('feedstock')['H2_yield'].mean().sort_values(ascending=False)
    feedstock_summary.head(8).plot(kind='bar', color='lightgreen', alpha=0.7)
    plt.title('Top 8 Feedstocks by H2 Yield')
    plt.ylabel('H2 Yield (mol/kg)')
    plt.xticks(rotation=45)
    
    # Temperature vs H2 yield
    plt.subplot(2, 2, 3)
    for tech in df_ml['gasifier_type'].unique():
        data = df_ml[df_ml['gasifier_type'] == tech]
        plt.scatter(data['temperature'], data['H2_yield'], label=tech, alpha=0.7, s=50)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('H2 Yield (mol/kg)')
    plt.title('Temperature vs H2 Yield by Technology')
    plt.legend()
    
    # Pressure vs H2 yield
    plt.subplot(2, 2, 4)
    for tech in df_ml['gasifier_type'].unique():
        data = df_ml[df_ml['gasifier_type'] == tech]
        plt.scatter(data['pressure'], data['H2_yield'], label=tech, alpha=0.7, s=50)
    plt.xlabel('Pressure (bar)')
    plt.ylabel('H2 Yield (mol/kg)')
    plt.title('Pressure vs H2 Yield by Technology')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    print("\n📊 Technology Summary:")
    print(tech_summary.round(2))
    
    return tech_summary

def make_predictions(best_model, X_input, y, model_name):
    """Make predictions and analyze model performance."""
    
    # Train on full dataset (small dataset approach)
    best_model.fit(X_input, y)
    y_pred = best_model.predict(X_input)
    
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    print(f"\n🎯 {model_name} Performance on Full Dataset:")
    print(f"R² Score: {r2:.3f}")
    print(f"RMSE: {rmse:.3f} mol/kg")
    
    # Plot predictions
    plt.figure(figsize=(8, 6))
    plt.scatter(y, y_pred, alpha=0.7, s=60, color='blue')
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    plt.xlabel('Actual H2 Yield (mol/kg)')
    plt.ylabel('Predicted H2 Yield (mol/kg)')
    plt.title(f'{model_name}: Actual vs Predicted H2 Yield (R² = {r2:.3f})')
    plt.grid(True, alpha=0.3)
    
    # Annotate points with technology
    for i, (actual, predicted) in enumerate(zip(y, y_pred)):
        if abs(actual - predicted) > rmse:  # Highlight large errors
            plt.annotate(f'{i}', (actual, predicted), xytext=(5, 5), 
                        textcoords='offset points', fontsize=8, color='red')
    
    plt.tight_layout()
    plt.show()
    
    return y_pred

def main():
    """Main function for improved gasification ML analysis."""
    print("🚀 Improved Gasification ML Analysis")
    print("=" * 50)
    
    # Load and prepare data
    print("\n1. Loading and preparing data...")
    X, y, le_gasifier, le_feedstock, df_ml = load_and_prepare_data()
    
    # Compare models
    print("\n2. Comparing ML models...")
    results, best_model_name = compare_models(X, y)
    
    # Feature importance analysis
    print("\n3. Analyzing feature importance...")
    feature_importance = analyze_feature_importance(X, y)
    
    # Technology analysis
    print("\n4. Analyzing gasification technologies...")
    tech_summary = create_technology_analysis(df_ml)
    
    # Make predictions with best model
    print("\n5. Making predictions with best model...")
    best_result = results[best_model_name]
    y_pred = make_predictions(
        best_result['model'], 
        best_result['X_input'], 
        y, 
        best_model_name
    )
    
    print(f"\n✨ Analysis complete!")
    print(f"🏆 Best approach: {best_model_name}")
    print(f"🎯 This approach is better suited for your small experimental dataset")
    
    return results, feature_importance, tech_summary

if __name__ == "__main__":
    results, feature_importance, tech_summary = main() 