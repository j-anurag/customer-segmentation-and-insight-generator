"""
segment_profiles.py — Visualization components for Streamlit.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_kpi_cards(df: pd.DataFrame):
    """Displays high-level KPIs about the segments."""
    st.markdown("### 📊 Customer Base Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    total_customers = len(df)
    total_segments = df['segment_name'].nunique()
    
    # Example KPIs - depending on the actual columns in UCI Bank dataset
    # Usually contains: age, balance, duration, campaign
    avg_age = df['age'].mean() if 'age' in df.columns else 0
    avg_balance = df['balance'].mean() if 'balance' in df.columns else 0
    
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Discovered Segments", total_segments)
    col3.metric("Avg Customer Age", f"{avg_age:.1f}")
    col4.metric("Avg Balance", f"€{avg_balance:,.0f}")

def render_segment_distribution(df: pd.DataFrame):
    """Shows the distribution of customers across segments."""
    st.markdown("### 🥧 Segment Distribution")
    segment_counts = df['segment_name'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    fig = px.pie(
        segment_counts, 
        values='Count', 
        names='Segment', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

def render_feature_analysis(df: pd.DataFrame):
    """Shows how features differ across segments."""
    st.markdown("### 📈 Feature Analysis by Segment")
    
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # Exclude internal ID columns
    numerical_cols = [c for c in numerical_cols if c not in ['id', 'cluster_id']]
    
    if not numerical_cols:
        st.warning("No numerical columns found for analysis.")
        return
        
    selected_feature = st.selectbox("Select a feature to analyze:", numerical_cols)
    
    fig = px.box(
        df, 
        x="segment_name", 
        y=selected_feature, 
        color="segment_name",
        title=f"Distribution of '{selected_feature}' across Segments"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def render_categorical_breakdown(df: pd.DataFrame):
    """Shows categorical breakdowns within segments."""
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    categorical_cols = [c for c in categorical_cols if c not in ['segment_name', 'cluster_id']]
    
    if not categorical_cols:
        return
        
    st.markdown("### 📊 Categorical Breakdown")
    selected_cat = st.selectbox("Select a categorical feature:", categorical_cols)
    
    # Calculate percentage distribution
    cross_tab = pd.crosstab(df['segment_name'], df[selected_cat], normalize='index') * 100
    
    fig = px.bar(
        cross_tab, 
        barmode='stack',
        title=f"{selected_cat.title()} Distribution by Segment (%)",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(yaxis_title="Percentage (%)", xaxis_title="Segment")
    st.plotly_chart(fig, use_container_width=True)
