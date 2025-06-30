import streamlit as st 
import pandas as pd 
import plotly.express as px 

df = pd.read_csv('data/campaign_metrics.csv')

df['CTR'] = df['clicks'] / df['impressions']
df['CPA'] = df['cost'] / df['conversions']

df['CTR'] = df['CTR'].apply(lambda x: f"{x:.2%}")
df['CPA'] = df['CPA'].apply(lambda x: f"${x:,.2f}")

st.sidebar.header("Filter the data")
channels = st.sidebar.multiselect(
    "Select channel(s):",
    options=df['channel'].unique(),
    default=df['channel'].unique()
)

from datetime import datetime

dates = sorted([
    datetime.strptime(date_str, "%Y-%m-%d").date()
    for date_str in df['campaign_date'].unique()
])

date_range = st.sidebar.slider(
    "Select date range:",
    min_value=min(dates),
    max_value=max(dates),
    value=(min(dates), max(dates))
)

df['campaign_date'] = pd.to_datetime(df['campaign_date'])

date_range = (pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))

filtered_df = df[
    (df['channel'].isin(channels)) &
    (df['campaign_date'] >= date_range[0]) &
    (df['campaign_date'] <= date_range[1])
]

st.title(" Marketing Campaign Performance Dashboard")

st.dataframe(filtered_df)

st.subheader("CTR Over Time by Channel")
fig_ctr = px.line(filtered_df, x='campaign_date', y='CTR', color='channel')
st.plotly_chart(fig_ctr)

st.subheader("CPA Over Time by Channel")
fig_cpa = px.line(filtered_df, x='campaign_date', y='CPA', color='channel')
st.plotly_chart(fig_cpa)

st.subheader(" Summary Metrics")
total_cost = filtered_df['cost'].sum()
total_conversions = filtered_df['conversions'].sum()
filtered_df['CTR'] = pd.to_numeric(filtered_df['CTR'], errors='coerce')
avg_ctr = filtered_df['CTR'].mean()
avg_cpa = total_cost / total_conversions if total_conversions > 0 else 0

st.write(f"**Total Cost:** ${total_cost:.2f}")
st.write(f"**Total Conversions:** {total_conversions}")
st.write(f"**Average CTR:** {avg_ctr:.2%}")
st.write(f"**Average CPA:** ${avg_cpa:.2f}")
