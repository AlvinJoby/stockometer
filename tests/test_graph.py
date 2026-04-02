import unittest

from graph import generate_graph

from tests.test_app import make_price_frame


class GraphTests(unittest.TestCase):
    def test_generate_graph_returns_html_for_supported_indicators(self):
        graph_html = generate_graph(
            make_price_frame(),
            ["RSI", "SMA_20", "EMA_20", "EMA_50", "EMA_100", "MACD"],
        )

        self.assertIn("plotly", graph_html.lower())
        self.assertIn("Open:", graph_html)


if __name__ == "__main__":
    unittest.main()
