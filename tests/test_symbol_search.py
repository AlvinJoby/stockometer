import unittest
from unittest.mock import patch

from symbol_search import normalize_quote, search_symbols


class NormalizeQuoteTests(unittest.TestCase):
    def test_returns_none_without_symbol(self):
        self.assertIsNone(normalize_quote({"shortname": "Apple Inc."}))

    def test_returns_none_for_disallowed_quote_type(self):
        self.assertIsNone(
            normalize_quote(
                {"symbol": "AAPL", "quoteType": "INDEX"},
                allowed_types={"EQUITY"},
            )
        )

    def test_prefers_shortname_and_normalizes_fields(self):
        result = normalize_quote(
            {
                "symbol": " AAPL ",
                "shortname": "Apple Inc.",
                "longname": "Apple Incorporated",
                "exchange": " NMS ",
                "quoteType": "equity",
            },
            allowed_types={"EQUITY"},
        )

        self.assertEqual(
            result,
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "exchange": "NMS",
                "type": "EQUITY",
            },
        )

    def test_falls_back_to_symbol_for_name(self):
        result = normalize_quote(
            {"symbol": "MSFT", "exchange": "NMS", "quoteType": "EQUITY"},
            allowed_types={"EQUITY"},
        )

        self.assertEqual(result["name"], "MSFT")


class SearchSymbolsTests(unittest.TestCase):
    def test_short_queries_return_empty_list(self):
        self.assertEqual(search_symbols("A"), [])
        self.assertEqual(search_symbols(" "), [])

    @patch("symbol_search.Search")
    def test_search_symbols_returns_filtered_deduped_results(self, mock_search):
        mock_search.return_value.quotes = [
            {
                "symbol": "AAPL",
                "shortname": "Apple Inc.",
                "exchange": "NMS",
                "quoteType": "EQUITY",
            },
            {
                "symbol": "AAPL",
                "shortname": "Apple Inc.",
                "exchange": "NMS",
                "quoteType": "EQUITY",
            },
            {
                "symbol": "SPY",
                "shortname": "SPDR S&P 500 ETF",
                "exchange": "PCX",
                "quoteType": "ETF",
            },
            {
                "symbol": "",
                "shortname": "Broken",
                "exchange": "NMS",
                "quoteType": "EQUITY",
            },
            {
                "symbol": "^GSPC",
                "shortname": "S&P 500",
                "exchange": "SNP",
                "quoteType": "INDEX",
            },
        ]

        results = search_symbols("app")

        self.assertEqual(
            results,
            [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "exchange": "NMS",
                    "type": "EQUITY",
                },
                {
                    "symbol": "SPY",
                    "name": "SPDR S&P 500 ETF",
                    "exchange": "PCX",
                    "type": "ETF",
                },
            ],
        )
        mock_search.assert_called_once()

    @patch("symbol_search.Search", side_effect=RuntimeError("upstream error"))
    def test_search_symbols_fail_closed_on_upstream_error(self, _mock_search):
        self.assertEqual(search_symbols("app"), [])
