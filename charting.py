from typing import Literal
import webbrowser
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from datetime import date

ChartType = Literal["line", "area", "candlestick"]

def filter_by_date(df: pd.DataFrame, begin: date, end: date) -> pd.DataFrame:
    mask = (df["date"] >= begin) & (df["date"] <= end)
    return df.loc[mask].sort_values("date")

def make_chart(df: pd.DataFrame, chart_type: ChartType, symbol: str, begin: date, end: date) -> str:
    title = f"{symbol} — {begin} to {end}"
    if chart_type == "candlestick" and all(c in df.columns for c in ["open", "high", "low", "close"]):
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df["date"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name=symbol
                )
            ]
        )
    elif chart_type == "area":
        y = df.get("adjusted_close", df.get("close"))
        fig = go.Figure(
            data=[go.Scatter(x=df["date"], y=y, fill="tozeroy", mode="lines", name=symbol)]
        )
    else:  # line
        y = df.get("adjusted_close", df.get("close"))
        fig = go.Figure(
            data=[go.Scatter(x=df["date"], y=y, mode="lines", name=symbol)]
        )

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    # Save to standalone HTML and open
    out_html = "chart.html"
    pio.write_html(fig, file=out_html, auto_open=False, include_plotlyjs="cdn")
    webbrowser.open_new_tab(out_html)
    return out_html
