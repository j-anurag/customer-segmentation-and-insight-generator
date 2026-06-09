"""
db.py — Database utility for the Streamlit dashboard.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from pathlib import Path

# Fallback to local SQLite if Postgres is not available
DB_PATH = Path(__file__).parent.parent.parent / "data" / "segmentation.db"

@st.cache_resource
def get_db_connection():
    use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"
    
    if use_sqlite:
        return create_engine(f"sqlite:///{DB_PATH}")
    else:
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5434")
        db_name = os.getenv("DB_NAME", "segmentation_db")
        db_user = os.getenv("DB_USER", "analyst")
        db_pass = os.getenv("DB_PASSWORD", "analytics_2024")
        conn_str = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        return create_engine(conn_str)

@st.cache_data(ttl=3600)
def fetch_segmented_data() -> pd.DataFrame:
    """Fetches the clustered customer data from the database."""
    engine = get_db_connection()
    query = "SELECT * FROM customer_segments"
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Failed to fetch data from database: {e}")
        return pd.DataFrame()
