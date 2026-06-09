"""
cluster.py — K-Means clustering model for customer segmentation.
"""

import logging
import pandas as pd
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

def train_clusters(df_features: pd.DataFrame, n_clusters: int = 4, random_state: int = 42) -> tuple[KMeans, pd.Series]:
    """
    Trains a K-Means clustering model.
    Returns:
        - The trained KMeans model
        - A Pandas Series of segment assignments
    """
    logger.info(f"Training K-Means model with {n_clusters} clusters...")
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    cluster_labels = kmeans.fit_predict(df_features)
    
    logger.info("Clustering complete.")
    return kmeans, pd.Series(cluster_labels, index=df_features.index, name="cluster_id")

def generate_segment_names(df_clean: pd.DataFrame, cluster_labels: pd.Series) -> pd.DataFrame:
    """
    Attaches business-friendly segment names based on cluster centroids or raw rules.
    In a real scenario, this involves analyzing the centroids. We'll map generic names for now.
    """
    df_result = df_clean.copy()
    df_result["cluster_id"] = cluster_labels
    
    # Generic names - in a real business case, we would profile the clusters first
    segment_map = {
        0: "Segment A - High Value",
        1: "Segment B - Core Customers",
        2: "Segment C - At Risk",
        3: "Segment D - Emerging"
    }
    
    df_result["segment_name"] = df_result["cluster_id"].map(segment_map)
    return df_result
