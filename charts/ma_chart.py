import plotly.graph_objects as go
from retrieveData import colname
import pandas as pd

def add_sma(fig,data,symbol,rows):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["sma_indicator"],
                mode="lines",
                name="SMA",
                line=dict(color="#facc15", width=2)
            ),
            row=rows, col=1
        )


def add_ema20(fig,data,symbol,rows):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["ema_20"],
                mode="lines",
                name="EMA_20",
                line=dict(color="#3b82f6", width=2)
            ),
            row=rows, col=1
        )