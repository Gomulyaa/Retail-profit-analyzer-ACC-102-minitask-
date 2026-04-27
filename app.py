import streamlit as st
import pandas as pd

# Import my other python files
from data_loader import load_data, get_data_summary
from filters import create_filters, apply_filters
from charts import (
    plot_profit_by_category, 
    plot_profit_margin, 
    plot_discount_vs_profit,
    plot_regional_profit,
    plot_segment_profit
)
from insights import generate_recommendations, identify_profit_killers_deep

# Page config
st.set_page_config(page_title="Profit Dashboard", layout="wide") 
df = load_data()
st.title("📊 Retail Profit Analyzer")
st.markdown("### A Profitability Diagnostic Tool for Retail Managers")

regions, segments, categories, discount_range = create_filters(df) # Sidebar filters
filtered = apply_filters(df, regions, segments, categories, discount_range)# Apply filters
col1, col2, col3, col4 = st.columns(4) # Key metrics

total_sales = filtered['Sales'].sum()
total_profit = filtered['Profit'].sum()
margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
loss_count = len(filtered[filtered['Profit'] < 0])

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📈 Total Profit", f"${total_profit:,.0f}")
col3.metric("📊 Profit Margin", f"{margin:.1f}%")
col4.metric("⚠️ Loss-Making Rows", f"{loss_count:,}")

st.divider()

# Charts Section
subcat_data = plot_profit_by_category(filtered)
plot_profit_margin(subcat_data)
plot_discount_vs_profit(filtered)

col_left, col_right = st.columns(2)
with col_left:
    region_data = plot_regional_profit(filtered)
with col_right:
    segment_data = plot_segment_profit(filtered)

st.divider()

# Insights Section
st.divider()
killers = identify_profit_killers_deep(filtered)
generate_recommendations(filtered, subcat_data, region_data, segment_data, killers)

st.divider()
st.caption(f"Data source is attained from Superstore Dataset | Currently showing {len(filtered):,} rows | User is able to filter using sidebar")