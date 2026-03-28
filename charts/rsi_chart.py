import plotly.graph_objects as go
import pandas as pd

def add_rsi(fig,data,rows):
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["RSI"],
                mode="lines",
                name="RSI",
                line=dict(color="#3b82f6", width=3)
            ),
            row=rows, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["buy_RSI"],
                mode="markers+text",
                text=[
                    "BUY" if pd.notna(val) else ""
                    for val in data["buy_RSI"]
                ],
                textposition="top center",
                marker=dict(symbol="triangle-up", color="#22c55e", size=12),
                name="Buy"
            ),
            row=rows, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["sell_RSI"],
                mode="markers+text",
                text=[
                    "SELL" if pd.notna(val) else ""
                    for val in data["sell_RSI"]
                ],
                textposition="bottom center",
                marker=dict(symbol="triangle-down", color="#ef4444", size=12),
                name="Sell"
            ),
            row=rows, col=1
        )

        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=rows, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=rows, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", row=rows, col=1)

        fig.update_yaxes(range=[0, 100], row=rows, col=1)