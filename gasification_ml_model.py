#!/usr/bin/env python3
"""
LCA Gasification Neural Network Regression
This script trains a scikit-learn neural network model to predict H₂ and CO yield 
from gasification process parameters.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.inspection import permutation_importance

def load_real_gasification_data():
    """Load real experimental gasification data from your research."""
    df = pd.read_csv('data/gasification_data_refined.csv')
    
    # Rename columns to match ML model expectations
    df_ml = df.rename(columns={
        'temperature_C': 'temperature',
        'reaction_time_min': 'reaction_time', 
        'pressure_bar': 'pressure',
        'agent_ratio': 'steam_ratio',
        'feedstock_type': 'feedstock',
        'technology': 'gasifier_type',
        'H2_yield_mol_kg': 'H2_yield',
        'CO_yield_mol_kg': 'CO_yield'
    })
    
    # Fill missing steam_ratio values with median
    df_ml['steam_ratio'] = df_ml['steam_ratio'].fillna(df_ml['steam_ratio'].median())
    
    # Fill missing CO_yield values (we'll focus on H2_yield prediction)
    df_ml['CO_yield'] = df_ml['CO_yield'].fillna(0)
    
    print(f"📊 Loaded real experimental data: {len(df_ml)} entries")
    print(f"🔬 Technologies: {df_ml['gasifier_type'].value_counts().to_dict()}")
    print(f"🌱 Feedstocks: {df_ml['feedstock'].nunique()} unique types")
    
    return df_ml

def preprocess_data(df):
    """Preprocess the data for machine learning."""
    # Define input features and output targets
    features = ["temperature", "reaction_time", "pressure", "steam_ratio", "feedstock", "gasifier_type"]
    
    # For now, focus on H2_yield prediction since we have complete data for it
    # Can extend to multi-output later when we have more complete CO_yield data
    targets = ["H2_yield"]
    
    X = df[features]
    y = df[targets]
    
    print(f"✅ Features: {features}")
    print(f"✅ Target: {targets}")
    
    # Preprocessing: Scale numeric + one-hot encode categorical
    numeric_features = ["temperature", "reaction_time", "pressure", "steam_ratio"]
    categorical_features = ["feedstock", "gasifier_type"]
    
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(sparse_output=False), categorical_features)
    ])
    
    X_processed = preprocessor.fit_transform(X)
    
    return X_processed, y, preprocessor

def train_model(X_train, y_train):
    """Train the neural network model."""
    # For single output (H2_yield), use MLPRegressor directly
    model = MLPRegressor(
        hidden_layer_sizes=(64, 32, 16),  # Smaller network for smaller dataset
        activation='relu',
        solver='adam',
        max_iter=2000,  # More iterations for better convergence
        random_state=42,
        early_stopping=True,
        validation_fraction=0.2,
        learning_rate_init=0.001,
        alpha=0.01  # L2 regularization to prevent overfitting
    )
    
    print("Training neural network for H2 yield prediction...")
    model.fit(X_train, y_train.values.ravel())  # Flatten y for single output
    
    # Print training information
    print(f"H2_yield prediction:")
    print(f"  - Iterations: {model.n_iter_}")
    print(f"  - Final loss: {model.loss_:.6f}")
    
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate the model performance."""
    y_pred = model.predict(X_test)
    
    # Calculate R² score for H2 yield
    r2_h2 = r2_score(y_test["H2_yield"], y_pred)
    
    # Calculate RMSE for H2 yield
    rmse_h2 = np.sqrt(mean_squared_error(y_test["H2_yield"], y_pred))
    
    print("\nModel Performance:")
    print(f"H2 Yield - R²: {r2_h2:.4f}, RMSE: {rmse_h2:.4f}")
    
    return y_pred, r2_h2, rmse_h2

def plot_results(y_test, y_pred, r2_h2):
    """Plot actual vs predicted results for H2 yield."""
    plt.figure(figsize=(8, 6))
    
    plt.scatter(y_test["H2_yield"], y_pred, alpha=0.7, color='blue', s=50)
    plt.plot([y_test["H2_yield"].min(), y_test["H2_yield"].max()], 
             [y_test["H2_yield"].min(), y_test["H2_yield"].max()], 'r--', lw=2)
    plt.title(f"Actual vs Predicted H2 Yield (R² = {r2_h2:.3f})")
    plt.xlabel("Actual H2 Yield (mol/kg)")
    plt.ylabel("Predicted H2 Yield (mol/kg)")
    plt.grid(True, alpha=0.3)
    
    # Add text annotations for some points
    for i, (actual, predicted) in enumerate(zip(y_test["H2_yield"], y_pred)):
        if i < 5:  # Annotate first 5 points
            plt.annotate(f'({actual:.1f}, {predicted:.1f})', 
                        (actual, predicted), xytext=(5, 5), 
                        textcoords='offset points', fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    plt.show()

def analyze_feature_importance(model, X_test, y_test, preprocessor):
    """Analyze feature importance using permutation importance."""
    print("\nAnalyzing feature importance for H2 yield prediction...")
    
    # Calculate permutation importance
    perm_importance = permutation_importance(model, X_test, y_test.values.ravel(), n_repeats=10, random_state=42)
    
    # Get feature names
    feature_names = preprocessor.get_feature_names_out()
    
    # Plot feature importance
    importances = perm_importance.importances_mean
    indices = np.argsort(importances)[::-1][:10]  # Top 10 features
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(indices)), importances[indices])
    plt.title('Top 10 Feature Importance - H2 Yield Prediction')
    plt.xlabel('Features')
    plt.ylabel('Permutation Importance')
    plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    print("\nTop 10 most important features for H2 yield:")
    for i, idx in enumerate(indices):
        print(f"{i+1}. {feature_names[idx]}: {importances[idx]:.4f}")

def main():
    """Main function to run the complete ML pipeline."""
    print("LCA Gasification Neural Network Regression")
    print("=" * 50)
    
    # Step 1: Load real experimental dataset
    print("\n1. Loading real experimental dataset...")
    df = load_real_gasification_data()
    print(f"Dataset loaded with shape: {df.shape}")
    print("\n🔬 Sample of your experimental data:")
    print(df.head())
    
    # Step 2: Preprocess data
    print("\n2. Preprocessing data...")
    X_processed, y, preprocessor = preprocess_data(df)
    print(f"Processed features shape: {X_processed.shape}")
    
    # Step 3: Train/test split
    print("\n3. Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Step 4: Train model
    print("\n4. Training model...")
    model = train_model(X_train, y_train)
    
    # Step 5: Evaluate model
    print("\n5. Evaluating model...")
    y_pred, r2_h2, rmse_h2 = evaluate_model(model, X_test, y_test)
    
    # Step 6: Plot results
    print("\n6. Plotting results...")
    plot_results(y_test, y_pred, r2_h2)
    
    # Step 7: Feature importance analysis
    print("\n7. Feature importance analysis...")
    analyze_feature_importance(model, X_test, y_test, preprocessor)
    
    print("\n" + "=" * 50)
    print("Analysis complete!")
    
    return model, preprocessor

if __name__ == "__main__":
    model, preprocessor = main() 