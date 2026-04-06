import pandas as pd

def get_range_levels(df, lookback=20):
    recent = df.iloc[:-1].tail(lookback)
    if recent.empty:
        recent = df.tail(lookback)
    return recent['High'].max(), recent['Low'].min()

def volume_confirmation(df, lookback=20):
    avg_vol = df['Volume'].iloc[:-1].tail(lookback).mean()
    if pd.isna(avg_vol) or avg_vol == 0:
        avg_vol = df['Volume'].tail(lookback).mean()
    current_vol = df['Volume'].iloc[-1]
    return current_vol > 1.5 * avg_vol

def breakout_engine(df, lookback=20):
    resistance, support = get_range_levels(df, lookback)
    close = df['Close'].iloc[-1]
    buffer = 0.005
    vol_ok = volume_confirmation(df, lookback)

    if close > resistance * (1 + buffer):
        return {
            "signal": "breakout",
            "level": resistance,
            "strength": "strong" if vol_ok else "weak"
        }

    elif close < support * (1 - buffer):
        return {
            "signal": "breakdown",
            "level": support,
            "strength": "strong" if vol_ok else "weak"
        }

    else:
        return {
            "signal": "range",
            "level": None,
            "strength": "low"
        }


def get_breakout_events(df, lookback=20):
    events = []

    for i in range(lookback, len(df) - 5):
        sub_df = df.iloc[:i]

        result = breakout_engine(sub_df, lookback)

        if result['signal'] in ['breakout', 'breakdown']:
            events.append({
                "index": i,
                "type": result['signal'],
                "level": result['level'],
                "price": sub_df['Close'].iloc[-1]
            })

    return events

def filter_duplicate_events(events, min_gap=5):
    filtered = []
    last_index = -100

    for e in events:
        if e['index'] - last_index >= min_gap:
            filtered.append(e)
            last_index = e['index']

    return filtered

def evaluate_events(events, df):
    for e in events:
        idx = e['index']
        entry = e['price']

        future_price = df['Close'].iloc[idx + 5]
        move = (future_price - entry) / entry

        if e['type'] == 'breakdown':
            move = -move

        e['return'] = move

    return events

def classify_events_adaptive(events, df, lookback=20, k_success=1.0, k_failure=0.7):
    df = df.copy()

    df['ret'] = df['Close'].pct_change()
    df['volatility'] = df['ret'].rolling(lookback).std()

    for e in events:
        idx = e['index']
        r = e['return']

        vol = df['volatility'].iloc[idx]

        if pd.isna(vol) or vol == 0:
            e['outcome'] = 'neutral'
            e['confidence'] = 0
            continue

        success_th = k_success * vol
        failure_th = -k_failure * vol

        if r > success_th:
            e['outcome'] = 'success'
        elif r < failure_th:
            e['outcome'] = 'failure'
        else:
            e['outcome'] = 'neutral'

        e['confidence'] = abs(r) / vol

    return events

def summarize(events):
    total = len(events)

    if total == 0:
        return {
            "total": 0,
            "success_rate": 0,
            "failure_rate": 0,
            "avg_return": 0,
            "avg_confidence": 0
        }

    success = [e for e in events if e['outcome'] == 'success']
    failure = [e for e in events if e['outcome'] == 'failure']

    avg_return = sum(e['return'] for e in events) / total
    avg_conf = sum(e.get('confidence', 0) for e in events) / total

    return {
        "total": total,
        "success_rate": round(len(success) / total, 2),
        "failure_rate": round(len(failure) / total, 2),
        "avg_return": round(avg_return, 4),
        "avg_confidence": round(avg_conf, 2)
    }

def recent_events(events, df, n=7):
    latest = events[-n:]

    output = []
    for e in latest:
        date = str(df.index[e['index']].date())

        output.append({
            "date": date,
            "type": e['type'],
            "return": round(e['return'] * 100, 2),
            "outcome": e['outcome'],
            "confidence": round(e.get('confidence', 0), 2)
        })

    return output


def breakout_behavior(df):
    df = df.tail(150).copy()

    events = get_breakout_events(df)
    events = filter_duplicate_events(events)
    events = evaluate_events(events, df)
    events = classify_events_adaptive(events, df)

    if len(events) == 0:
        return {
            "summary": {"note": "Low data"},
            "recent": []
        }

    summary = summarize(events)
    recent = recent_events(events, df)

    return {
        "summary": summary,
        "recent": recent
    }
