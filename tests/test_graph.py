import unittest
import pandas as pd

from graph import _compute_price_axis_range, generate_graph

from tests.test_app import make_price_frame


class GraphTests(unittest.TestCase):
    def test_compute_price_axis_range_preserves_normal_chart_range(self):
        frame = make_price_frame()
        visible_data = frame[frame.index >= frame.index[-1] - pd.DateOffset(months=6)]

        axis_range = _compute_price_axis_range(visible_data)

        expected_min = float(visible_data["Low"].min())
        expected_max = float(visible_data["High"].max())
        expected_padding = (expected_max - expected_min) * 0.1

        self.assertEqual(
            axis_range,
            [expected_min - expected_padding, expected_max + expected_padding],
        )

    def test_compute_price_axis_range_ignores_extreme_outlier_spike(self):
        frame = make_price_frame()
        frame.loc[frame.index[30], "High"] = 800.0
        frame.loc[frame.index[30], "Low"] = 790.0

        visible_data = frame[frame.index >= frame.index[-1] - pd.DateOffset(months=6)]
        axis_range = _compute_price_axis_range(visible_data)

        self.assertLess(axis_range[1], 300.0)
        self.assertGreater(axis_range[1], float(visible_data["Close"].iloc[-1]))

    def test_generate_graph_returns_html_for_supported_indicators(self):
        graph_html = generate_graph(
            make_price_frame(),
            ["RSI", "SMA_20", "EMA_20", "EMA_50", "EMA_100", "MACD"],
        )

        self.assertIn("plotly", graph_html.lower())
        self.assertIn("Open:", graph_html)
        self.assertNotIn("BUY", graph_html)
        self.assertNotIn("SELL", graph_html)


if __name__ == "__main__":
    unittest.main()
