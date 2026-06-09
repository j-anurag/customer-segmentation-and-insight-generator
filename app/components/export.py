"""
export.py — CSV export functionality for Streamlit.
"""

import pandas as pd
import streamlit as st

def render_export_section(df: pd.DataFrame):
    """Renders a section allowing the user to download the segment data."""
    st.markdown("### 📥 Export Insights")
    st.write("Download the fully segmented dataset for further marketing campaigns or CRM imports.")
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Segmented Data (CSV)",
        data=csv_data,
        file_name="customer_segments_export.csv",
        mime="text/csv",
        type="primary"
    )
