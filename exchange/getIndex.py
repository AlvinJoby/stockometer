EXCHANGE_TO_INDEX = {
    "NSE": "^NSEI",
    "BSE": "^BSESN",

    "NMS": "^GSPC",
    "NYQ": "^GSPC",
    "ASE": "^GSPC",

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


def get_index(exchange: str) -> str:
    if not exchange:
        return None

    exchange = exchange.upper().strip()

    index = EXCHANGE_TO_INDEX.get(exchange)

    if not index and exchange in US_EXCHANGES:
        index = "^GSPC"

    return index