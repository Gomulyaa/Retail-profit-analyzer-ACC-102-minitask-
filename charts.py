import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def plot_profit_by_category(filtered):
    st.subheader("Profit by Product Sub-Category")
    
    subcat_data = filtered.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    subcat_data['Margin'] = (subcat_data['Profit'] / subcat_data['Sales'] * 100).round(1)
    subcat_data = subcat_data.sort_values('Profit', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['red' if x < 0 else 'green' for x in subcat_data['Profit']]
    ax.bar(subcat_data['Sub-Category'], subcat_data['Profit'], color=colors)
    ax.set_ylabel('Profit ($)')
    ax.set_xlabel('Product Sub-Category')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    
    return subcat_data

def plot_profit_margin(subcat_data):
    st.subheader("Profit Margin by Sub-Category")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors_margin = ['red' if x < 0 else 'green' for x in subcat_data['Margin']]
    ax.bar(subcat_data['Sub-Category'], subcat_data['Margin'], color=colors_margin)
    ax.set_ylabel('Profit Margin (%)')
    ax.set_xlabel('Product Sub-Category')
    ax.tick_params(axis='x', rotation=45)
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    st.pyplot(fig)

import plotly.express as px

def plot_discount_vs_profit(filtered):
    st.subheader("Discount vs Profit Analysis")
    
    # Create interactive plot
    fig = px.scatter(
        filtered,
        x='Discount',
        y='Profit',
        hover_data=['Sub-Category', 'Region', 'Segment', 'Category'],
        color='Sub-Category',
        title='Hover over any dot to see product details'
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    fig.update_layout(
        xaxis_title="Discount (%)",
        yaxis_title="Profit ($)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    high_discount_loss = filtered[(filtered['Discount'] > 0.3) & (filtered['Profit'] < 0)]
    if len(high_discount_loss) > 0:
        st.warning(f"⚠️ {len(high_discount_loss)} transactions had >30% discount AND lost money")
    else:
        st.success("No high-discount transactions are losing money")

def plot_regional_profit(filtered):
    st.subheader("Profit by Region")
    
    region_data = filtered.groupby('Region')['Profit'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_reg = ['red' if x < 0 else 'green' for x in region_data['Profit']]
    ax.bar(region_data['Region'], region_data['Profit'], color=colors_reg)
    ax.set_ylabel('Profit ($)')
    st.pyplot(fig)
    
    return region_data

def plot_segment_profit(filtered):
    st.subheader("Profit by Customer Segment")
    
    segment_data = filtered.groupby('Segment')['Profit'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_seg = ['red' if x < 0 else 'green' for x in segment_data['Profit']]
    ax.bar(segment_data['Segment'], segment_data['Profit'], color=colors_seg)
    ax.set_ylabel('Profit ($)')
    st.pyplot(fig)
    
    return segment_data