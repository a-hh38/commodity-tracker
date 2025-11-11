import streamlit as st
import pandas as pd
import plotly.express as px
from fetch_data import get_data, commodities  

st.set_page_config(page_title="Commodities Tracker", layout="wide")
st.title("Commodities Tracker Dashboard")
st.markdown("Track and compare the latest commodity prices with charts and analytics. \nHover cursor around charts to get detailed values")

st.sidebar.header("Filters")
selected_commodities = st.sidebar.multiselect(
    "Select Commodities",
    options=list(commodities.keys()),
    default=["Gold", "Silver"]
)
period = st.sidebar.selectbox("Select Period", options=["1mo", "3mo", "6mo", "1y"], index=2)
interval = st.sidebar.selectbox("Select Interval", options=["1d", "1wk"], index=0)

data_frames = []
for name in selected_commodities:
    try:
        df = get_data(commodities[name], name, period, interval)  
        data_frames.append(df)
    except Exception as e:
        st.warning(f"Failed to fetch data for {name}: {e}")

if not data_frames:
    st.error("No data to display. Check your commodity selections or internet connection.")
    st.stop()

data = pd.concat(data_frames, axis=1).ffill()

if isinstance(data.columns, pd.MultiIndex):
    data.columns = [col[0] for col in data.columns]

st.subheader("Commodity Prices Over Time")
fig = px.line(data, x=data.index, y=data.columns, title="Commodity Price Over Time")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Normalized Prices Comparison (Base=100)")
normalized = data / data.iloc[0] * 100
fig_norm = px.line(normalized, x=normalized.index, y=normalized.columns, title="Normalized Prices")
st.plotly_chart(fig_norm, use_container_width=True)

st.subheader("Moving Averages (7-day & 30-day)")
ma7 = data.rolling(window=7).mean()
ma30 = data.rolling(window=30).mean()

fig_ma = px.line()
for col in data.columns:
    fig_ma.add_scatter(x=data.index, y=data[col], mode='lines', name=f"{col} Price")
    fig_ma.add_scatter(x=ma7.index, y=ma7[col], mode='lines', name=f"{col} MA7")
    fig_ma.add_scatter(x=ma30.index, y=ma30[col], mode='lines', name=f"{col} MA30")
st.plotly_chart(fig_ma, use_container_width=True)

st.subheader("Percent Change Analysis")
percent_change = ((data.ffill().iloc[-1] - data.ffill().iloc[0]) / data.ffill().iloc[0]) * 100
st.dataframe(percent_change.round(2).rename("Percent Change (%)"))

# Footer
st.markdown("---")
st.markdown(f"Built by Athharva Patil, using Streamlit and yfinance | Data as of {pd.Timestamp.now().strftime('%Y-%m-%d | GMT: %H+5:%M+30:%S')}")






