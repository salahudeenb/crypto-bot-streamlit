import os
import streamlit as st
import pandas as pd
import ccxt
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Crypto Bot", layout="wide")

st.title("Crypto Trading Bot — Streamlit App")

# Sidebar controls
st.sidebar.header("Settings")
MODE = st.sidebar.selectbox("Mode", ["paper", "live"], index=0)
EXCHANGE_ID = st.sidebar.selectbox("Exchange", ["binance", "kraken", "coinbasepro"], index=0)
SYMBOL = st.sidebar.text_input("Trading Pair", value="BTC/USDT")
TIMEFRAME = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=1)
FAST_EMA = st.sidebar.number_input("Fast EMA", min_value=1, value=9)
SLOW_EMA = st.sidebar.number_input("Slow EMA", min_value=1, value=21)
SIZE_USD = st.sidebar.number_input("Trade Size (USD)", min_value=1.0, value=50.0)
LIMIT = st.sidebar.slider("OHLCV Limit", min_value=50, max_value=1000, value=200, step=50)
st.sidebar.markdown("---")
st.sidebar.markdown("**Secure credentials** (live mode)")
API_KEY = st.sidebar.text_input("API Key", value=os.getenv("API_KEY", ""), type="password")
API_SECRET = st.sidebar.text_input("API Secret", value=os.getenv("API_SECRET", ""), type="password")
USE_SANDBOX = st.sidebar.checkbox("Use exchange sandbox/testnet (if supported)", value=False)

def create_exchange(exchange_id, api_key="", api_secret="", sandbox=False):
    params = {"enableRateLimit": True}
    if api_key and api_secret:
        params["apiKey"] = api_key
        params["secret"] = api_secret
    exchange_cls = getattr(ccxt, exchange_id)
    exchange = exchange_cls(params)
    try:
        if sandbox and hasattr(exchange, 'set_sandbox_mode'):
            exchange.set_sandbox_mode(True)
    except Exception:
        pass
    return exchange

@st.cache_data(ttl=30)
def fetch_ohlcv_cached(exchange_id, symbol, timeframe, limit):
    exchange = create_exchange(exchange_id)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def apply_strategy(df, fast, slow):
    df = df.copy()
    df["ema_fast"] = ema(df["close"], fast)
    df["ema_slow"] = ema(df["close"], slow)
    df["signal"] = 0
    df.loc[df["ema_fast"] > df["ema_slow"], "signal"] = 1
    df["signal_shift"] = df["signal"].shift(1).fillna(0)
    df["entry"] = ((df["signal"] == 1) & (df["signal_shift"] == 0)).astype(int)
    df["exit"] = ((df["signal"] == 0) & (df["signal_shift"] == 1)).astype(int)
    return df

st.sidebar.markdown("---")
st.sidebar.markdown("**Actions**")
run = st.sidebar.button("Fetch & Run Strategy")
st.sidebar.write("Built: {}".format(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")))

if run:
    try:
        with st.spinner("Fetching market data..."):
            df = fetch_ohlcv_cached(EXCHANGE_ID, SYMBOL, TIMEFRAME, LIMIT)
    ex
                       
