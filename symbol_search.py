from difflib import SequenceMatcher

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


def score_symbol_match(query, item):
    normalized_query = (query or "").strip().lower()
    if not normalized_query:
        return 0

    symbol = item["symbol"].lower()
    name = " ".join(item["name"].lower().split())

    score = 0

    if symbol == normalized_query:
        score += 200
    elif symbol.startswith(normalized_query):
        score += 140
    elif normalized_query in symbol:
        score += 90

    if name == normalized_query:
        score += 220
    elif name.startswith(normalized_query):
        score += 170
    elif normalized_query in name:
        score += 120

    tokens = name.replace(".", " ").replace(",", " ").split()
    if any(token.startswith(normalized_query) for token in tokens):
        score += 80

    score += int(SequenceMatcher(None, normalized_query, symbol).ratio() * 70)
    score += int(SequenceMatcher(None, normalized_query, name).ratio() * 100)

    return score


def search_symbols(query, max_results=8, allowed_types=None):
    normalized_query = (query or "").strip()
    if len(normalized_query) < 2:
        return []

    allowed_types = allowed_types or ALLOWED_QUOTE_TYPES

    try:
        results = Search(
            query=normalized_query,
            max_results=max(max_results * 3, 20),
            news_count=0,
            lists_count=0,
            include_cb=False,
            include_nav_links=False,
            include_research=False,
            include_cultural_assets=False,
            enable_fuzzy_query=True,
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

    symbols.sort(
        key=lambda item: (
            score_symbol_match(normalized_query, item),
            item["name"].lower(),
            item["symbol"],
        ),
        reverse=True,
    )

    return symbols[:max_results]
