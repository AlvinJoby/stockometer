import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots
from retrieveData import colname


def generate_graph(data, symbol, show_rsi=False):

    # Create figure depending on RSI selection
    if show_rsi:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.04,
            row_heights=[0.7, 0.3]
        )
    else:
        fig = go.Figure()

    # -----------------------
    # Candlestick chart
    # -----------------------

    candle = go.Candlestick(
        x=data.index,
        open=data[colname(symbol, "Open")],
        high=data[colname(symbol, "High")],
        low=data[colname(symbol, "Low")],
        close=data[colname(symbol, "Close")],
        name="Price",

        increasing=dict(
            line=dict(color="#22c55e", width=1),
            fillcolor="#22c55e"
        ),
        decreasing=dict(
            line=dict(color="#ef4444", width=1),
            fillcolor="#ef4444"
        ),

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
            row=2,
            col=1
        )

        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", row=2, col=1)

        fig.update_yaxes(range=[0, 100], row=2, col=1)


    # -----------------------
    # Layout
    # -----------------------

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#06090f",
        plot_bgcolor="#05080e",
        dragmode="pan",
        hovermode="x unified",
        height=650 if show_rsi else 520,
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

    graph_html = pio.to_html(
        fig,
        full_html=False,
        config={
            "scrollZoom": True,
            "displaylogo": False,
            "displayModeBar": False,
            "responsive": True
        }
    )

    return graph_html