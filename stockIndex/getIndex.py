EXCHANGE_TO_INDEX = {
    "NSE": "NIFTYBEES.NS",
    "NSI": "NIFTYBEES.NS",
    "BSE": "NIFTYBEES.NS",
    "BOM": "NIFTYBEES.NS",

    "NMS": "SPY",
    "NYQ": "SPY",
    "ASE": "SPY",
    "PCX": "SPY",

    "LSE": "EWU",
    "TYO": "EWJ",
    "HKG": "EWH",

    "SHH": "ASHR",
    "SHE": "ASHR",

    "FRA": "EWG",
    "PAR": "EWQ",
    "TOR": "EWC",
    "ASX": "EWA",
    "KSC": "EWY",
    "SAO": "EWZ",
    "JNB": "EZA",
}

US_EXCHANGES = {"NMS", "NYQ", "ASE", "PCX"}

SUFFIX_TO_INDEX = {
    ".NS": "NIFTYBEES.NS",
    ".BO": "NIFTYBEES.NS",
    ".L": "EWU",
    ".T": "EWJ",
    ".HK": "EWH",
    ".SS": "ASHR",
    ".SZ": "ASHR",
    ".PA": "EWQ",
    ".F": "EWG",
    ".TO": "EWC",
    ".AX": "EWA",
    ".KS": "EWY",
    ".SA": "EWZ",
    ".JO": "EZA",
}

INDEX_DISPLAY_NAMES = {
    "SPY": "S&P 500 (ETF)",
    "NIFTYBEES.NS": "NIFTY 50 (ETF)",
    "EWU": "UK Market (ETF)",
    "EWJ": "Japan Market (ETF)",
    "EWH": "Hong Kong Market (ETF)",
    "ASHR": "China Market (ETF)",
    "EWG": "Germany Market (ETF)",
    "EWQ": "France Market (ETF)",
    "EWC": "Canada Market (ETF)",
    "EWA": "Australia Market (ETF)",
    "EWY": "Korea Market (ETF)",
    "EWZ": "Brazil Market (ETF)",
    "EZA": "South Africa Market (ETF)",
}


def get_index(exchange: str, symbol: str = None) -> str:
    normalized_exchange = (exchange or "").upper().strip()

    if normalized_exchange:
        index = EXCHANGE_TO_INDEX.get(normalized_exchange)

        if not index and normalized_exchange in US_EXCHANGES:
            index = "SPY"

        if index:
            return index

    normalized_symbol = (symbol or "").upper().strip()

    for suffix, index in SUFFIX_TO_INDEX.items():
        if normalized_symbol.endswith(suffix):
            return index

    return None


def get_index_display_name(index_ticker: str) -> str:
    if not index_ticker:
        return None

    return INDEX_DISPLAY_NAMES.get(index_ticker, index_ticker)