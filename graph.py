import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots
from retrieveData import colname


def generate_graph(data, symbol, show_rsi=True):

    # -----------------------
    # Create Figure
    # -----------------------
    if show_rsi:
        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            row_heights=[0.6, 0.2, 0.2]
        )
    else:
        fig = go.Figure()

    # -----------------------
    # Candlestick
    # -----------------------
    candle = go.Candlestick(
        x=data.index,
        open=data[colname(symbol, "Open")],
        high=data[colname(symbol, "High")],
        low=data[colname(symbol, "Low")],
        close=data[colname(symbol, "Close")],
        name="Price",
        increasing=dict(line=dict(color="#22c55e", width=1), fillcolor="#22c55e"),
        decreasing=dict(line=dict(color="#ef4444", width=1), fillcolor="#ef4444"),
        hovertemplate=(
            "Open: %{open:.2f}<br>"
            "High: %{high:.2f}<br>"
            "Low: %{low:.2f}<br>"
            "Close: %{close:.2f}"
            "<extra></extra>"
        )
    )

    if show_rsi:
        fig.add_trace(candle, row=1, col=1)
    else:
        fig.add_trace(candle)

    # -----------------------
    # SMA + EMA
    # -----------------------
    if show_rsi:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["sma_indicator"],
                mode="lines",
                name="SMA",
                line=dict(color="#facc15", width=3)
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["ema_20"],
                mode="lines",
                name="EMA",
                line=dict(color="#21AB21", width=3)
            ),
            row=1, col=1
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["sma_indicator"],
                mode="lines",
                name="SMA",
                line=dict(color="#facc15", width=3)
            )
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["ema_20"],
                mode="lines",
                name="EMA",
                line=dict(color="#21AB21", width=3)
            )
        )

    # -----------------------
    # RSI PANEL
    # -----------------------
    if show_rsi:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["RSI"],
                mode="lines",
                name="RSI",
                line=dict(color="#3b82f6", width=3)
            ),
            row=2, col=1
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
            row=2, col=1
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
            row=2, col=1
        )

        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", row=2, col=1)

        fig.update_yaxes(range=[0, 100], row=2, col=1)

    # -----------------------
    # MACD PANEL
    # -----------------------
    if show_rsi:

        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data["macd_histogram"],
                name="MACD Histogram",
                marker=dict(
                    color=[
                        "#22c55e" if (pd.notna(val) and val >= 0)
                        else "#ef4444" if (pd.notna(val) and val < 0)
                        else "#000000"
                        for val in data["macd_histogram"]
                    ]
                )
            ),
            row=3, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["macd_indicator"],
                mode="lines",
                name="MACD",
                line=dict(color="#3b82f6", width=2)
            ),
            row=3, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["macd_ema"],
                mode="lines",
                name="Signal",
                line=dict(color="#facc15", width=2)
            ),
            row=3, col=1
        )

        fig.add_hline(y=0, line_dash="dot", line_color="gray", row=3, col=1)

    # -----------------------
    # Layout
    # -----------------------
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#06090f",
        plot_bgcolor="#05080e",
        dragmode="pan",
        hovermode="x unified",
        height=750 if show_rsi else 600,
        margin=dict(l=10, r=10, t=20, b=40),
        showlegend=False
    )

    fig.update_layout(xaxis_rangeslider_visible=False)

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showspikes=True,
        spikecolor="gray",
        spikemode="across",
        spikesnap="cursor"
    )

    fig.update_yaxes(
        side="right",
        tickformat=".2f",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
        showspikes=True,
        spikecolor="gray",
        spikemode="across",
        spikesnap="cursor"
    )

    fig.update_yaxes(fixedrange=True)

    # -----------------------
    # Zoom (6 months)
    # -----------------------
    end_date = data.index[-1]
    start_date = end_date - pd.DateOffset(months=6)

    visible_data = data[data.index >= start_date]
    y_min = float(visible_data[colname(symbol, "Low")].min())
    y_max = float(visible_data[colname(symbol, "High")].max())
    padding = (y_max - y_min) * 0.05

    fig.update_xaxes(range=[start_date, end_date], fixedrange=False)

    if show_rsi:
        fig.update_yaxes(
            range=[y_min - padding, y_max + padding],
            fixedrange=False,
            row=1, col=1
        )
    else:
        fig.update_yaxes(
            range=[y_min - padding, y_max + padding],
            fixedrange=False
        )

    # -----------------------
    # Export HTML
    # -----------------------
    graph_html = pio.to_html(
        fig,
        full_html=False,
        config={
            "scrollZoom": False,
            "displaylogo": False,
            "displayModeBar": False,
            "responsive": True
        }
    )

    return graph_html