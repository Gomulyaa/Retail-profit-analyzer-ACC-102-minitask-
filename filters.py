import streamlit as st

def create_filters(df):
    st.sidebar.header("Filters")
    
    regions = st.sidebar.multiselect(
        "Region",
        df['Region'].unique(),
        default=df['Region'].unique()
    )
    
    segments = st.sidebar.multiselect(
        "Customer Segment",
        df['Segment'].unique(),
        default=df['Segment'].unique()
    )
    
    categories = st.sidebar.multiselect(
        "Product Category",
        df['Category'].unique(),
        default=df['Category'].unique()
    )
    
    discount_range = st.sidebar.slider(
        "Discount Range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.05
    )
    
    return regions, segments, categories, discount_range

def apply_filters(df, regions, segments, categories, discount_range):
    filtered = df[
        df['Region'].isin(regions) &
        df['Segment'].isin(segments) &
        df['Category'].isin(categories) &
        (df['Discount'] >= discount_range[0]) &
        (df['Discount'] <= discount_range[1])
    ]
    return filtered