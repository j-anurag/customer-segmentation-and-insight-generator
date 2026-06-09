"""
fetch_data.py — Downloads the UCI Bank Marketing Dataset.
"""

import logging
from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"

def fetch_bank_data() -> pd.DataFrame:
    """Fetches dataset from UCI and returns as Pandas DataFrame."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = DATA_DIR / "bank_marketing_raw.csv"

    if cache_path.exists():
        logger.info(f"Loading dataset from cache: {cache_path}")
        return pd.read_csv(cache_path)

    logger.info("Downloading dataset from UCI Machine Learning Repository (ID 222)...")
    try:
        # fetch dataset 
        bank_marketing = fetch_ucirepo(id=222)
        
        # data (as pandas dataframes) 
        df = bank_marketing.data.original
        
        # Save to cache
        df.to_csv(cache_path, index=False)
        logger.info(f"Dataset downloaded and cached to {cache_path}")
        
        return df
    except Exception as e:
        logger.error(f"Failed to fetch dataset: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = fetch_bank_data()
    print(df.head())
    print(df.info())
