import plotly.graph_objects as go
import pandas as pd

def add_sma(fig,data,rows):
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


def add_ema20(fig,data,rows):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["ema_20"],
                mode="lines",
                name="EMA_20",
                line=dict(color="#00E5FF", width=2)
            ),
            row=rows, col=1
        )

def add_ema50(fig,data,rows):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["ema_50"],
                mode="lines",
                name="EMA_50",
                line=dict(color="#2962FF", width=2)
            ),
            row=rows, col=1
        )

def add_ema100(fig,data,rows):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["ema_100"],
                mode="lines",
                name="EMA_100",
                line=dict(color="#1A237E", width=2)
            ),
            row=rows, col=1
        )