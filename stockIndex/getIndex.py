EXCHANGE_TO_INDEX = {
    "NSE": "^NSEI",
    "NSI": "^NSEI",
    "BSE": "^BSESN",
    "BOM": "^BSESN",

    "NMS": "^GSPC",
    "NYQ": "^GSPC",
    "ASE": "^GSPC",
    "PCX": "^GSPC",

    "LSE": "^FTSE",
    "TYO": "^N225",
    "HKG": "^HSI",

    "SHH": "000001.SS",
    "SHE": "399001.SZ",

    "FRA": "^GDAXI",
    "PAR": "^FCHI",
    "TOR": "^GSPTSE",
    "ASX": "^AXJO",
    "KSC": "^KS11",
    "SAO": "^BVSP",
    "JNB": "^JN0U.JO",
}

US_EXCHANGES = {"NMS", "NYQ", "ASE", "PCX"}

SUFFIX_TO_INDEX = {
    ".NS": "^NSEI",
    ".BO": "^BSESN",
    ".L": "^FTSE",
    ".T": "^N225",
    ".HK": "^HSI",
    ".SS": "000001.SS",
    ".SZ": "399001.SZ",
    ".PA": "^FCHI",
    ".F": "^GDAXI",
    ".TO": "^GSPTSE",
    ".AX": "^AXJO",
    ".KS": "^KS11",
    ".SA": "^BVSP",
    ".JO": "^JN0U.JO",
}

INDEX_DISPLAY_NAMES = {
    "^NSEI": "NIFTY 50",
    "^BSESN": "SENSEX",
    "^GSPC": "S&P 500",
    "^FTSE": "FTSE 100",
    "^N225": "NIKKEI 225",
    "^HSI": "HANG SENG",
    "000001.SS": "SSE COMPOSITE",
    "399001.SZ": "SZSE COMPONENT",
    "^GDAXI": "DAX",
    "^FCHI": "CAC 40",
    "^GSPTSE": "S&P/TSX COMPOSITE",
    "^AXJO": "S&P/ASX 200",
    "^KS11": "KOSPI",
    "^BVSP": "IBOVESPA",
    "^JN0U.JO": "FTSE/JSE TOP 40",
}


def get_index(exchange: str, symbol: str = None) -> str:
    normalized_exchange = (exchange or "").upper().strip()

    if normalized_exchange:
        index = EXCHANGE_TO_INDEX.get(normalized_exchange)

        if not index and normalized_exchange in US_EXCHANGES:
            index = "^GSPC"

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
