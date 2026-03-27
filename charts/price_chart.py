import plotly.graph_objects as go
from retrieveData import colname


def add_price(fig, data, symbol, rows):

    fig.add_trace(
        go.Candlestick(
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
        ),
        row=rows,
        col=1
    )