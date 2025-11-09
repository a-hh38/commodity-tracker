# fetch_data.py
import yfinance as yf
import pandas as pd

# Commodity tickers
commodities = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Crude Oil": "CL=F",
    "Natural Gas": "NG=F",
    "Copper": "HG=F"
}

def get_data(ticker, name, period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)[["Close"]]
    data.index = pd.to_datetime(data.index)
    data.columns = [name]  # ensure single-level column
    data = data.ffill()  # forward-fill missing data
    return data
