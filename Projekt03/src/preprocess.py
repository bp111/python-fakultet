import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def preprocess_data(df):
    print("--- Starting Data Preprocessing ---")
        
    # customerID is unique to everyone and carries no predictive pattern; drop
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
            
    # Looks like a string
    # Force it to numeric and fill the resulting NaNs with 0, since they haven't paid yet
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
            
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
    X = df.drop('Churn', axis=1) # Features
    y = df['Churn'] # Target
        
    # Categories like 'InternetService' into binary columns
    X_encoded = pd.get_dummies(X, drop_first=True)
    print(f"Shape after One-Hot Encoding: {X_encoded.shape}")
        
    # Split before scaling, to prevent test data influencing scaler
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
        
    scaler = StandardScaler() # Normalization/Standarization
        
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
        
    # Keep 95% of the information while reducing the number of columns
    # (dimensionality reduction)
    pca = PCA(n_components=0.95, random_state=42)
    X_train_pca = pca.fit_transform(X_train_scaled)
    X_test_pca = pca.transform(X_test_scaled)
    
    print(f"Original feature count: {X_train_scaled.shape[1]}")
    print(f"Reduced feature count (PCA): {X_train_pca.shape[1]}")
    print("--- Preprocessing Complete ---")
    
    return X_train_pca, X_test_pca, y_train, y_test, scaler, pca

if __name__ == "__main__":
    df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    X_train, X_test, y_train, y_test, scaler, pca = preprocess_data(df)