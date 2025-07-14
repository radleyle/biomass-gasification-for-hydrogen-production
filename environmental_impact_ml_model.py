#!/usr/bin/env python3
"""
Environmental Impact Prediction Model for Biomass Gasification
Standalone ML model that predicts 18 environmental impact indicators from operational parameters
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

def load_operational_data():
    """Load operational gasification data from CSV."""
    print("🔬 Loading operational gasification data...")
    
    df = pd.read_csv('data/gasification_data_refined.csv')
    
    print(f"✅ Operational data loaded: {df.shape}")
    print(f"🔍 Technologies: {df['technology'].unique()}")
    print(f"🔍 Key parameters available:")
    print(f"   - Temperature: {df['temperature_C'].min():.0f}-{df['temperature_C'].max():.0f}°C")
    print(f"   - H2 yield: {df['H2_yield_mol_kg'].min():.1f}-{df['H2_yield_mol_kg'].max():.1f} mol/kg")
    print(f"   - CO yield: {df['CO_yield_mol_kg'].min():.1f}-{df['CO_yield_mol_kg'].max():.1f} mol/kg")
    
    return df

def load_environmental_impact_data():
    """Load environmental impact data to use as training targets."""
    print("\n🌍 Loading environmental impact target data...")
    
    lca_df = pd.read_excel('data/LCA/LCAResultsWithWaste.xlsx')
    lca_df.columns = [col.strip() for col in lca_df.columns]
    
    # Rename technology columns to match operational data
    column_mapping = {
        'CO2 Gasfication': 'co2',
        'Plasma Gasification': 'plasma', 
        'SCWG': 'scw',
        'Steam Gasification': 'steam'
    }
    lca_df = lca_df.rename(columns=column_mapping)
    
    print(f"✅ Environmental impact data loaded: {lca_df.shape}")
    print(f"🔍 Impact categories: {lca_df.shape[0]}")
    print(f"🔍 Technologies: {[col for col in lca_df.columns if col != 'Impact categories']}")
    
    return lca_df

def create_training_dataset(operational_df, impact_df):
    """Create training dataset by mapping operational parameters to environmental impacts."""
    print("\n🔗 Creating training dataset...")
    
    # Get technology averages from operational data for mapping
    tech_averages = operational_df.groupby('technology').agg({
        'temperature_C': 'mean',
        'pressure_bar': 'mean',
        'H2_yield_mol_kg': 'mean',
        'CO_yield_mol_kg': 'mean',
        'reaction_time_min': 'mean'
    }).reset_index()
    
    # Create training rows - one for each technology
    training_data = []
    
    for _, tech_row in tech_averages.iterrows():
        tech = tech_row['technology']
        
        # Get environmental impacts for this technology
        if tech in impact_df.columns:
            impacts = impact_df[tech].values
            
            # Create feature vector
            features = {
                'technology': tech,
                'temperature_C': tech_row['temperature_C'],
                'pressure_bar': tech_row['pressure_bar'],
                'H2_yield_mol_kg': tech_row['H2_yield_mol_kg'],
                'CO_yield_mol_kg': tech_row['CO_yield_mol_kg'],
                'reaction_time_min': tech_row['reaction_time_min']
            }
            
            # Add all environmental impact values
            for i, impact_category in enumerate(impact_df['Impact categories']):
                features[f'impact_{i:02d}_{impact_category.replace(" ", "_").lower()}'] = impacts[i]
            
            training_data.append(features)
    
    # Also add individual operational data points with interpolated impacts
    for _, op_row in operational_df.iterrows():
        tech = op_row['technology']
        
        if tech in impact_df.columns:
            impacts = impact_df[tech].values
            
            features = {
                'technology': tech,
                'temperature_C': op_row['temperature_C'],
                'pressure_bar': op_row['pressure_bar'],
                'H2_yield_mol_kg': op_row['H2_yield_mol_kg'],
                'CO_yield_mol_kg': op_row['CO_yield_mol_kg'],
                'reaction_time_min': op_row['reaction_time_min']
            }
            
            # Add environmental impact values (same for all points of same technology)
            for i, impact_category in enumerate(impact_df['Impact categories']):
                features[f'impact_{i:02d}_{impact_category.replace(" ", "_").lower()}'] = impacts[i]
            
            training_data.append(features)
    
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Training dataset created: {training_df.shape}")
    print(f"🔍 Features: {len([col for col in training_df.columns if not col.startswith('impact_')])}")
    print(f"🔍 Target variables: {len([col for col in training_df.columns if col.startswith('impact_')])}")
    
    return training_df, list(impact_df['Impact categories'])

def prepare_features_and_targets(training_df, impact_categories):
    """Prepare feature matrix and target variables for ML training."""
    print("\n🛠️ Preparing features and targets...")
    
    # Feature columns (operational parameters)
    feature_cols = ['temperature_C', 'pressure_bar', 'H2_yield_mol_kg', 'CO_yield_mol_kg', 'reaction_time_min']
    
    # Technology encoding
    le_tech = LabelEncoder()
    tech_encoded = le_tech.fit_transform(training_df['technology'])
    
    # Create feature matrix
    X = training_df[feature_cols].copy()
    X['technology_encoded'] = tech_encoded
    
    # Create target matrix (all environmental impacts)
    impact_cols = [col for col in training_df.columns if col.startswith('impact_')]
    y = training_df[impact_cols].values
    
    print(f"✅ Feature matrix: {X.shape}")
    print(f"✅ Target matrix: {y.shape}")
    print(f"🔍 Features: {list(X.columns)}")
    
    return X, y, le_tech, impact_cols

def train_environmental_impact_model(X, y, impact_categories):
    """Train machine learning model to predict environmental impacts."""
    print("\n🤖 Training environmental impact prediction model...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Handle NaN values by filling with median
    from sklearn.impute import SimpleImputer
    imputer = SimpleImputer(strategy='median')
    X_train_scaled = imputer.fit_transform(X_train_scaled)
    X_test_scaled = imputer.transform(X_test_scaled)
    
    # Try multiple models (focusing on ones that work well with our data)
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
        'Ridge (Multi-output)': MultiOutputRegressor(Ridge(alpha=1.0))
    }
    
    best_model = None
    best_score = -np.inf
    best_name = ""
    results = {}
    
    for name, model in models.items():
        print(f"\n📊 Training {name}...")
        
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Predict
        y_pred = model.predict(X_test_scaled)
        
        # Evaluate
        r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
        mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
        mae = mean_absolute_error(y_test, y_pred, multioutput='uniform_average')
        
        print(f"   R² Score: {r2:.3f}")
        print(f"   MSE: {mse:.3e}")
        print(f"   MAE: {mae:.3e}")
        
        results[name] = {
            'model': model,
            'r2': r2,
            'mse': mse,
            'mae': mae,
            'predictions': y_pred
        }
        
        if r2 > best_score:
            best_score = r2
            best_model = model
            best_name = name
    
    print(f"\n🏆 Best model: {best_name} (R² = {best_score:.3f})")
    
    return best_model, scaler, imputer, results, X_test, y_test

def analyze_model_performance(model, X_test, y_test, impact_categories):
    """Analyze model performance for each environmental impact category."""
    print("\n📈 Analyzing model performance by impact category...")
    
    y_pred = model.predict(X_test)
    
    # Calculate R² for each impact category
    impact_r2_scores = []
    for i in range(y_test.shape[1]):
        try:
            r2 = r2_score(y_test[:, i], y_pred[:, i])
            # Handle edge cases where all predictions are the same (zero variance)
            if np.isnan(r2):
                r2 = 0.0
            impact_r2_scores.append(r2)
        except:
            impact_r2_scores.append(0.0)
    
    # Create performance DataFrame
    performance_df = pd.DataFrame({
        'Impact_Category': impact_categories,
        'R2_Score': impact_r2_scores
    }).sort_values('R2_Score', ascending=False)
    
    print("\n🎯 Model Performance by Environmental Impact:")
    print("=" * 60)
    for _, row in performance_df.head(10).iterrows():
        print(f"{row['Impact_Category']:<40} R² = {row['R2_Score']:.3f}")
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Average R² Score: {np.mean(impact_r2_scores):.3f}")
    print(f"   Best R² Score: {np.max(impact_r2_scores):.3f}")
    print(f"   Worst R² Score: {np.min(impact_r2_scores):.3f}")
    
    return performance_df

def analyze_feature_importance(model, feature_names):
    """Analyze feature importance for the trained model."""
    print("\n🔍 Analyzing feature importance...")
    
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        # Create feature importance DataFrame
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        print("\n🔝 Top Feature Importances:")
        print("=" * 40)
        for _, row in importance_df.iterrows():
            print(f"{row['Feature']:<25} {row['Importance']:.1%}")
        
        return importance_df
    else:
        print("ℹ️  Feature importance not available for this model type")
        return None

def save_model(model, scaler, imputer, le_tech, impact_categories, feature_names):
    """Save the trained model and preprocessing objects."""
    print("\n💾 Saving trained model...")
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'imputer': imputer,
        'label_encoder': le_tech,
        'impact_categories': impact_categories,
        'feature_names': feature_names
    }
    
    joblib.dump(model_data, 'environmental_impact_model.pkl')
    print("✅ Model saved as 'environmental_impact_model.pkl'")

def predict_environmental_impacts(temperature_C, pressure_bar, H2_yield, CO_yield, reaction_time, technology, 
                                model, scaler, imputer, le_tech, impact_categories):
    """Make environmental impact predictions for new operational parameters."""
    
    # Encode technology
    try:
        tech_encoded = le_tech.transform([technology])[0]
    except ValueError:
        print(f"❌ Unknown technology: {technology}")
        print(f"Available technologies: {list(le_tech.classes_)}")
        return None
    
    # Create feature vector
    features = np.array([[temperature_C, pressure_bar, H2_yield, CO_yield, reaction_time, tech_encoded]])
    
    # Scale features
    features_scaled = scaler.transform(features)
    
    # Handle any NaN values
    features_scaled = imputer.transform(features_scaled)
    
    # Predict
    predictions = model.predict(features_scaled)[0]
    
    # Create results DataFrame
    results = pd.DataFrame({
        'Impact_Category': impact_categories,
        'Predicted_Value': predictions
    })
    
    return results

def create_visualizations(performance_df, importance_df=None):
    """Create visualizations for model performance."""
    print("\n📊 Creating visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Model Performance by Impact Category
    ax1 = axes[0, 0]
    performance_df_plot = performance_df.head(15)  # Top 15 for readability
    bars = ax1.barh(range(len(performance_df_plot)), performance_df_plot['R2_Score'])
    ax1.set_yticks(range(len(performance_df_plot)))
    ax1.set_yticklabels([cat[:30] + '...' if len(cat) > 30 else cat for cat in performance_df_plot['Impact_Category']])
    ax1.set_xlabel('R² Score')
    ax1.set_title('Model Performance by Environmental Impact')
    ax1.grid(axis='x', alpha=0.3)
    
    # Color bars based on performance
    for i, bar in enumerate(bars):
        score = performance_df_plot.iloc[i]['R2_Score']
        if score >= 0.8:
            bar.set_color('green')
        elif score >= 0.6:
            bar.set_color('orange')
        else:
            bar.set_color('red')
    
    # 2. Feature Importance (if available)
    if importance_df is not None:
        ax2 = axes[0, 1]
        ax2.pie(importance_df['Importance'], labels=importance_df['Feature'], autopct='%1.1f%%')
        ax2.set_title('Feature Importance Distribution')
    else:
        axes[0, 1].text(0.5, 0.5, 'Feature Importance\nNot Available', ha='center', va='center', fontsize=14)
        axes[0, 1].set_title('Feature Importance')
    
    # 3. Performance Distribution
    ax3 = axes[1, 0]
    ax3.hist(performance_df['R2_Score'], bins=10, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('R² Score')
    ax3.set_ylabel('Number of Impact Categories')
    ax3.set_title('Distribution of Model Performance')
    ax3.axvline(performance_df['R2_Score'].mean(), color='red', linestyle='--', 
                label=f'Mean: {performance_df["R2_Score"].mean():.3f}')
    ax3.legend()
    
    # 4. Performance Categories (handle negative R² scores)
    ax4 = axes[1, 1]
    performance_bins = pd.cut(performance_df['R2_Score'], 
                             bins=[-float('inf'), 0, 0.5, 0.7, 0.85, 1.0], 
                             labels=['Very Poor\n(<0)', 'Poor\n(0-0.5)', 'Fair\n(0.5-0.7)', 'Good\n(0.7-0.85)', 'Excellent\n(>0.85)'])
    performance_counts = performance_bins.value_counts()
    # Filter out any NaN categories
    performance_counts = performance_counts.dropna()
    colors = ['darkred', 'red', 'orange', 'lightgreen', 'darkgreen'][:len(performance_counts)]
    if len(performance_counts) > 0:
        ax4.pie(performance_counts.values, labels=performance_counts.index, autopct='%1.1f%%', colors=colors)
        ax4.set_title('Model Performance Categories')
    else:
        ax4.text(0.5, 0.5, 'No Valid\nPerformance Data', ha='center', va='center', fontsize=14)
        ax4.set_title('Model Performance Categories')
    
    plt.tight_layout()
    plt.savefig('environmental_impact_model_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Visualizations saved as 'environmental_impact_model_analysis.png'")

def main():
    """Main function to run the environmental impact ML model."""
    print("🌍 Environmental Impact Prediction Model for Biomass Gasification")
    print("=" * 70)
    
    # Load data
    operational_df = load_operational_data()
    impact_df = load_environmental_impact_data()
    
    # Create training dataset
    training_df, impact_categories = create_training_dataset(operational_df, impact_df)
    
    # Prepare features and targets
    X, y, le_tech, impact_cols = prepare_features_and_targets(training_df, impact_categories)
    
    # Train model
    model, scaler, imputer, results, X_test, y_test = train_environmental_impact_model(X, y, impact_categories)
    
    # Analyze performance
    performance_df = analyze_model_performance(model, X_test, y_test, impact_categories)
    
    # Analyze feature importance
    importance_df = analyze_feature_importance(model, list(X.columns))
    
    # Save model
    save_model(model, scaler, imputer, le_tech, impact_categories, list(X.columns))
    
    # Create visualizations
    create_visualizations(performance_df, importance_df)
    
    # Example prediction
    print("\n🔮 Example Prediction:")
    print("=" * 40)
    example_prediction = predict_environmental_impacts(
        temperature_C=600, pressure_bar=1, H2_yield=45, CO_yield=30, 
        reaction_time=15, technology='steam',
        model=model, scaler=scaler, imputer=imputer, le_tech=le_tech, impact_categories=impact_categories
    )
    
    if example_prediction is not None:
        print("Top 5 Environmental Impacts:")
        for _, row in example_prediction.head().iterrows():
            print(f"  {row['Impact_Category']}: {row['Predicted_Value']:.3e}")
    
    print("\n🎉 Environmental Impact Prediction Model Complete!")
    print(f"📊 Model Performance: R² = {np.mean(performance_df['R2_Score']):.3f}")
    print("💾 Model saved and ready for use!")

if __name__ == "__main__":
    main() 