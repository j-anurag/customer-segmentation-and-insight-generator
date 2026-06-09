"""
preprocess.py — Data Preprocessing and Feature Engineering.
Uses techniques from the senior-data-scientist skill.
"""

import logging
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

logger = logging.getLogger(__name__)

def build_feature_pipeline(numeric_cols, categorical_cols):
    """
    Returns a fitted-ready ColumnTransformer for structured tabular data.
    """
    numeric_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale",  StandardScaler()),
    ])
    
    categorical_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    
    transformers = [
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols),
    ]
    return ColumnTransformer(transformers, remainder="drop")

def preprocess_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, ColumnTransformer]:
    """
    Cleans and preprocesses the bank marketing dataset for clustering.
    Returns:
        - cleaned raw DataFrame (for visualization/DB)
        - transformed feature DataFrame (for modeling)
        - the fitted ColumnTransformer pipeline
    """
    logger.info("Starting data preprocessing...")
    df_clean = df.copy()

    # The UCI Bank Marketing dataset typically contains a target 'y'.
    # For clustering (unsupervised), we don't use 'y' for training, but keep it for profiling.
    target_col = 'y' if 'y' in df_clean.columns else None
    
    # Identify feature columns
    features_to_drop = ['y'] if target_col else []
    
    # Define numeric and categorical columns dynamically
    numeric_cols = df_clean.drop(columns=features_to_drop, errors='ignore').select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df_clean.drop(columns=features_to_drop, errors='ignore').select_dtypes(include=['object', 'category']).columns.tolist()
    
    logger.info(f"Identified {len(numeric_cols)} numeric and {len(categorical_cols)} categorical features.")

    # Build and fit pipeline
    pipeline = build_feature_pipeline(numeric_cols, categorical_cols)
    
    X_transformed = pipeline.fit_transform(df_clean)
    
    # Recover feature names after OneHotEncoding
    cat_encoder = pipeline.named_transformers_['cat'].named_steps['encode']
    encoded_cat_cols = cat_encoder.get_feature_names_out(categorical_cols)
    all_feature_names = numeric_cols + list(encoded_cat_cols)
    
    df_features = pd.DataFrame(X_transformed, columns=all_feature_names, index=df_clean.index)
    
    logger.info("Preprocessing complete.")
    return df_clean, df_features, pipeline
