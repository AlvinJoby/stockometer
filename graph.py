import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from retrieveData import colname

def generate_graph(data,symbol):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[colname(symbol,"Close")],
        mode="lines",
        name="Close Price"
    ))

    fig.update_layout(
        title=f"{symbol} Close Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )

    graph_html = pio.to_html(fig, full_html=False)

    return graph_html


