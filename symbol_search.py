from yfinance import Search


ALLOWED_QUOTE_TYPES = {"EQUITY", "ETF", "MUTUALFUND"}


def normalize_quote(quote, allowed_types=None):
    symbol = (quote.get("symbol") or "").strip()
    if not symbol:
        return None

    quote_type = (quote.get("quoteType") or "").strip().upper()
    if allowed_types and quote_type not in allowed_types:
        return None

    name = (
        (quote.get("shortname") or "").strip() or
        (quote.get("longname") or "").strip() or
        symbol
    )

    return {
        "symbol": symbol,
        "name": name,
        "exchange": (quote.get("exchange") or "").strip(),
        "type": quote_type,
    }


def search_symbols(query, max_results=8, allowed_types=None):
    normalized_query = (query or "").strip()
    if len(normalized_query) < 2:
        return []

    allowed_types = allowed_types or ALLOWED_QUOTE_TYPES

    try:
        results = Search(
            query=normalized_query,
            max_results=max_results,
            news_count=0,
            lists_count=0,
            include_cb=False,
            include_nav_links=False,
            include_research=False,
            include_cultural_assets=False,
            enable_fuzzy_query=False,
            recommended=0,
            raise_errors=True,
        )
    except Exception:
        return []

    symbols = []
    seen = set()

    for quote in getattr(results, "quotes", []) or []:
        normalized = normalize_quote(quote, allowed_types=allowed_types)
        if not normalized:
            continue
        symbol = normalized["symbol"]
        if symbol in seen:
            continue
        seen.add(symbol)
        symbols.append(normalized)

    return symbols
