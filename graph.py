import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots

from charts.price_chart import add_price
from charts.ma_chart import add_sma,add_ema20,add_ema50,add_ema100
from charts.rsi_chart import add_rsi
from charts.macd_chart import add_macd

OVERLAY_INDICATORS = {
    "SMA_20": add_sma,
    "EMA_20": add_ema20,
    "EMA_50": add_ema50,
    "EMA_100": add_ema100,
}

PANEL_INDICATORS = {
    "RSI": add_rsi,
    "MACD": add_macd,
}

def _compute_price_axis_range(visible_data):
    low_series = visible_data["Low"].dropna()
    high_series = visible_data["High"].dropna()

    if low_series.empty or high_series.empty:
        return None

    y_min = float(low_series.min())
    y_max = float(high_series.max())
    full_span = y_max - y_min

    robust_low = float(low_series.quantile(0.05))
    robust_high = float(high_series.quantile(0.95))
    robust_span = robust_high - robust_low

    recent_window = min(len(visible_data), 20)
    recent_low = float(low_series.tail(recent_window).min())
    recent_high = float(high_series.tail(recent_window).max())

    # Ignore one-off visible-range spikes only when they severely compress
    # the chart; otherwise preserve the full price range behavior.
    if robust_span > 0 and full_span > robust_span * 3:
        y_min = min(robust_low, recent_low)
        y_max = max(robust_high, recent_high)

    span = y_max - y_min
    reference_price = float(visible_data["Close"].dropna().iloc[-1]) if visible_data["Close"].dropna().size else y_max
    padding = span * 0.1 if span > 0 else max(reference_price * 0.02, 1.0)

    return [y_min - padding, y_max + padding]

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
        showlegend=False,

        hoverlabel=dict(
            bgcolor="#0d1117",
            bordercolor="#1e2330",
            font=dict(
                family="Inter, monospace",
                size=12,
                color="#e2e8f0"
            ),
            namelength=-1
        )
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
    price_axis_range = _compute_price_axis_range(visible_data)

    fig.update_xaxes(range=[start_date, end_date], fixedrange=False)

    if price_axis_range is not None:
        fig.update_yaxes(
                range=price_axis_range,
                autorange=False,
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
