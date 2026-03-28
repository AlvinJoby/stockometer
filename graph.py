import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots

from charts.price_chart import add_price
from charts.ma_chart import add_ema20,add_sma
from charts.rsi_chart import add_rsi
from charts.macd_indicator import add_macd

OVERLAY_INDICATORS = {
    "SMA_20": add_sma,
    "EMA_20": add_ema20,
}

PANEL_INDICATORS = {
    "RSI": add_rsi,
    "MACD": add_macd,
}

def generate_graph(data, indicators=None):

    if indicators is None:
        indicators = []

    overlay_inds = [i for i in indicators if i in OVERLAY_INDICATORS]
    panel_inds = [i for i in indicators if i in PANEL_INDICATORS]
    
    #layout-calculation

    rows = 1 + len(panel_inds)

    
    row_heights = [3] + [1] * len(panel_inds)

    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=row_heights
    )

    #row-mapping

    row_map = {"PRICE": 1}

    current_row = 2

    for ind in panel_inds:
        row_map[ind] = current_row
        current_row += 1

    add_price(fig, data, rows=row_map["PRICE"])

    for ind in overlay_inds:
        OVERLAY_INDICATORS[ind](fig, data, rows=row_map["PRICE"])

    for ind in panel_inds:
        PANEL_INDICATORS[ind](fig, data, rows=row_map[ind])

    if len(panel_inds)>0:
        height = 400 + (rows - 1) * 150
    else:
        height = 570

    # -----------------------
    # Layout
    # -----------------------
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#06090f",
        plot_bgcolor="#05080e",
        dragmode="pan",
        hovermode="x unified",
        height=height,
        margin=dict(l=10, r=60, t=20, b=40),
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
    y_min = float(visible_data["Low"].min())
    y_max = float(visible_data["High"].max())
    padding = (y_max - y_min) * 0.05

    fig.update_xaxes(range=[start_date, end_date], fixedrange=False)

    fig.update_yaxes(
            range=[y_min - padding, y_max + padding],
            fixedrange=False,
            row=1, col=1
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