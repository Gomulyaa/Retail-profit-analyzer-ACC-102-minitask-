import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv('superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

def get_data_summary(df):
    return {
        'total_rows': len(df),
        'total_sales': df['Sales'].sum(),
        'total_profit': df['Profit'].sum(),
        'margin': (df['Profit'].sum() / df['Sales'].sum() * 100)
    }