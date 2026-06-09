"""
load.py — Saves the segmented dataset to the database.
"""

import logging
import os
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

logger = logging.getLogger(__name__)

# Fallback to local SQLite if Postgres is not available
DB_PATH = Path(__file__).parent.parent / "data" / "segmentation.db"

def get_engine():
    # Check if Postgres is explicitly requested and available via ENV
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5434")
    db_name = os.getenv("DB_NAME", "segmentation_db")
    db_user = os.getenv("DB_USER", "analyst")
    db_pass = os.getenv("DB_PASSWORD", "analytics_2024")
    
    # Simple check: If running in a fully configured environment, try PG.
    # Otherwise, fallback to SQLite for local development ease.
    use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"
    
    if use_sqlite:
        logger.info(f"Using local SQLite database at {DB_PATH}")
        return create_engine(f"sqlite:///{DB_PATH}")
    else:
        logger.info(f"Attempting connection to PostgreSQL at {db_host}:{db_port}")
        conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        return create_engine(conn_str)

def load_to_db(df: pd.DataFrame, table_name: str = "customer_segments"):
    """
    Saves the dataframe to the database.
    """
    engine = get_engine()
    
    logger.info(f"Loading {len(df)} records into '{table_name}' table...")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    logger.info("Database load complete.")
