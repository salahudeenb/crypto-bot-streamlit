import os
import streamlit as st
import pandas as pd
import ccxt
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
import plotly.graph_objects as go

fig = go.Figure()


fig.add_trace(go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='OHLC'
))

fig.add_trace(go.Scatter(
    x=df['timestamp'],
    y=df['ema_fast'],
    line=dict(color='blue', width=1),
    name=f'EMA {FAST_EMA}'
))

fig.add_trace(go.S
    x=df['timestamp'],
    y=df['ema_slow'],
    line=dict(color='orange', width=1),
    name=f'EMA {SLOW_EMA}'
))

# Volume as bar chart on a secondary y-axis
fig.add_trace(go.Bar(
    x=df['timestamp'],
    y=df['volume'],
    name='Volume',
    marker_color='lightgray',
    yaxis='y2',
    opacity=0.3,
))

# Update layout to add volume y-axis
fig.update_layout(
    xaxis_rangeslider_visible=False,
    yaxis_title='Price',
    yaxis2=dict(
        title='Volume',
        overlaying='y',
        side='right',
        showgrid=False,
        position=0.15,
        range=[0, df['volume'].max() * 5]  # adjust range for visibility
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(l=40, r=40, t=40, b=40),
    height=500,
)

st.plotly_chart(fig, use_container_width=True)
