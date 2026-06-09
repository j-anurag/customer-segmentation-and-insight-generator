"""
run.py — Orchestrator for the Customer Segmentation Pipeline
"""

import logging
import sys
from dotenv import load_dotenv

from pipeline.fetch_data import fetch_bank_data
from pipeline.preprocess import preprocess_data
from pipeline.cluster import train_clusters, generate_segment_names
from pipeline.load import load_to_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("pipeline_runner")

def main():
    load_dotenv()
    logger.info("Starting Customer Segmentation Pipeline...")

    try:
        # 1. Fetch Data
        logger.info("[1/4] Fetching Data...")
        df_raw = fetch_bank_data()
        
        # 2. Preprocess & Feature Engineering
        logger.info("[2/4] Preprocessing & Feature Engineering...")
        df_clean, df_features, pipeline = preprocess_data(df_raw)
        
        # 3. K-Means Clustering
        logger.info("[3/4] Clustering Customers...")
        kmeans_model, cluster_labels = train_clusters(df_features, n_clusters=4)
        df_segmented = generate_segment_names(df_clean, cluster_labels)
        
        # 4. Load to Database
        logger.info("[4/4] Loading to Database...")
        load_to_db(df_segmented)
        
        logger.info("==================================================")
        logger.info("Pipeline Execution Completed Successfully!")
        logger.info(f"Total Customers Processed: {len(df_segmented)}")
        logger.info("==================================================")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
