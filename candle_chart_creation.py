"""Module for creating a candlestick chart for stock data."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def draw_candle_chart(df: pd.DataFrame, stock_symbol: str) -> None:
    """Draw a candlestick chart for the stock data.
    
    :param `pd.DataFrame` df: The stock data to plot.
    :param `str` stock_symbol: The stock symbol to display.
    
    :return: None
    """
    df['tradingDate'] = pd.to_datetime(df['tradingDate'], errors='coerce')
    df.set_index('tradingDate', inplace=True)

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.10, subplot_titles=(f'{stock_symbol} Price', 'Volume'),
        row_width=[0.2, 0.7]
    )

    fig.add_trace(go.Candlestick(
        x=df.index, open=df["openPrice"], high=df["highestPrice"],
        low=df["lowestPrice"], close=df["closePrice"], name="OHLC"
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=df.index, y=df['totalMatchVol'], marker_color='red', showlegend=False
    ), row=2, col=1)

    fig.update_layout(
        title=f'{stock_symbol} PT1D Candlestick Chart',
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price (Vnd/share)',
            titlefont_size=14,
            tickfont_size=12,
        ),
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        paper_bgcolor='LightSteelBlue'
    )

    # Explicitly set x-axis range to match the DataFrame's datetime range
    min_date = df.index.min()
    max_date = df.index.max()
    fig.update_xaxes(
        range=[min_date, max_date],
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True)
    )

    fig.update(layout_xaxis_rangeslider_visible=True)
    fig.show()
