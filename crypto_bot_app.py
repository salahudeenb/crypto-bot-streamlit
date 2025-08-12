import os
import streamlit as st
import pandas as pd
import ccxt
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
import plotly.graph_objects as go

load_dotenv()

st.set_page_config(page_title="Crypto Bot with Charts", layout="wide")
st.title("Crypto Trading Bot with Candlestick Chart")

# Sidebar - User inputs
st.sidebar.header("Settings")
EXCHANGE_ID = st.sidebar.selectbox("Exchange", ["binance", "kraken", "coinbasepro"], index=0)
SYMBOL = st.sidebar.text_input("Trading Pair", value="BTC/USDT")
TIMEFRAME = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=1)
FAST_EMA = st.sidebar.number_input("Fast EMA", min_value=1, value=9)
SLOW_EMA = st.sidebar.number_input("Slow EMA", min_value=1, value=21)
FAST_EMA = st.sidebar.number_input("Fast EMA", min_value=1, value=9)
SLOW_EMA = st.sidebar.number_input("Slow EMA", min_value=1, value=21)
LIMIT = st.sidebar.slider("Data points limit", 50, 1000, 200, 50)
