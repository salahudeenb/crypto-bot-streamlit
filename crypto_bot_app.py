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
