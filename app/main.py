"""
main.py — Streamlit Dashboard Entrypoint for Customer Segmentation.
"""

import sys
from pathlib import Path
import streamlit as st

# Add project root to python path to allow absolute imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from app.utils.db import fetch_segmented_data
from app.components.segment_profiles import (
    render_kpi_cards, 
    render_segment_distribution, 
    render_feature_analysis,
    render_categorical_breakdown
)
from app.components.export import render_export_section

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Segmentation Insights",
    page_icon="👥",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Custom CSS for Premium Design
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main container background */
    .stApp {
        background-color: #f8f9fc;
    }
    
    /* KPI Card styling */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1F497D !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #5c6c7f !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1F497D;
        font-family: 'Inter', sans-serif;
    }
    
    /* Subtly style the export button */
    .stDownloadButton button {
        background-color: #1F497D !important;
        color: white !important;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stDownloadButton button:hover {
        background-color: #16365d !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Application Layout
# ---------------------------------------------------------------------------
def main():
    st.title("👥 Customer Segmentation Insights")
    st.markdown("Explore AI-driven customer groups derived from the Bank Marketing dataset using K-Means clustering.")
    
    # Load data
    with st.spinner("Loading segmented customer data from database..."):
        df = fetch_segmented_data()
        
    if df.empty:
        st.error("No data found in the database. Please run the ML pipeline (`python -m pipeline.run`) first.")
        return
        
    # Main Dashboard UI
    st.divider()
    render_kpi_cards(df)
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_segment_distribution(df)
        
    with col2:
        render_categorical_breakdown(df)
        
    st.divider()
    render_feature_analysis(df)
    
    st.divider()
    render_export_section(df)

if __name__ == "__main__":
    main()
