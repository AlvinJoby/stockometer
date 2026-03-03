import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from retrieveData import colname

def generate_graph(data, symbol):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
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
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#06090f",
        plot_bgcolor="#05080e",
        dragmode="pan",
        hovermode="x unified",
        height=520,
        margin=dict(l=10, r=10, t=20, b=40),

        showlegend=False
    )

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