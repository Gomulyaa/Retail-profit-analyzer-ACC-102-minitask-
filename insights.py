import streamlit as st
import pandas as pd

def identify_profit_killers_deep(filtered):
    st.subheader("Profit Killers Deep Dive")
    
    killers = filtered[filtered['Profit'] < 0].groupby(['Sub-Category', 'Region', 'Segment']).agg({
        'Profit': 'sum',
        'Discount': 'mean',
        'Sales': 'sum'
    }).reset_index()
    killers = killers.sort_values('Profit', ascending=True).head(5)
    
    if len(killers) > 0:
        st.write("Top 5 Products with Combinations of Discount with the Biggest losses:")
        st.dataframe(killers)
        st.caption("Negative profit with high discount indicates pricing issue")
    else:
        st.success("No profit-killing combinations found!")
    
    return killers

def generate_recommendations(filtered, subcat_data, region_data, segment_data, killers):
    st.subheader("Business Recommendations")
    st.markdown("---")
    
    recommendations = []
    
    if len(killers) > 0:
        worst = killers.iloc[0]
        recommendations.append(f"High-priority: {worst['Sub-Category']} in {worst['Region']} region is losing ${abs(worst['Profit']):,.0f} with {worst['Discount']*100:.0f}% avg discount")
    
    high_discount_loss = filtered[(filtered['Discount'] > 0.3) & (filtered['Profit'] < 0)]
    if len(high_discount_loss) > 0:
        recommendations.append(f"Discount policy: {len(high_discount_loss)} transactions lost money despite >30% discounts. Implement discount caps.")
    else:
        recommendations.append("Discount policy: Current discount strategy seems healthy")
    
    top3 = subcat_data.nlargest(3, 'Profit')
    top_names = ', '.join(top3['Sub-Category'].tolist())
    recommendations.append(f"Invest more: {top_names} are your most profitable categories")
    
    worst_region = region_data[region_data['Profit'] == region_data['Profit'].min()]
    if len(worst_region) > 0 and worst_region.iloc[0]['Profit'] < 0:
        recommendations.append(f"Regional action: {worst_region.iloc[0]['Region']} region is losing money. Investigate costs.")
    
    worst_segment = segment_data[segment_data['Profit'] == segment_data['Profit'].min()]
    if len(worst_segment) > 0 and worst_segment.iloc[0]['Profit'] < 0:
        recommendations.append(f"Segment review: {worst_segment.iloc[0]['Segment']} segment is underperforming")
    
    for rec in recommendations:
        st.info(rec)
    
    st.markdown("---")
    st.subheader("Action Plan Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Stop / Reduce:**")
        for _, row in killers.head(2).iterrows():
            st.write(f"- {row['Sub-Category']} (discounts >{row['Discount']*100:.0f}%)")
    
    with col2:
        st.markdown("**Promote / Scale:**")
        for _, row in top3.iterrows():
            st.write(f"- {row['Sub-Category']}")