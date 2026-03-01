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
        name="Close Price",
        hovertemplate="%{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        #title=dict(text=f"{symbol}",
        #           font=dict(size=26)),
        #xaxis_title="Date",
        #yaxis_title="Price",
        yaxis=dict(side="right",tickformat=".2f"),
        template="plotly_dark",
        dragmode="pan",
        hovermode="x unified",
        height=600,
        margin=dict(l=20,r=30)
    )

    graph_html = pio.to_html(fig,
                             full_html=False,
                             config={
                                 "scrollZoom":True,
                                 "displaylogo":False,
                                 "displayModeBar": False
                             })

    return graph_html


