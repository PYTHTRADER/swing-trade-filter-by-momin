# swing scanner script
def compute_indicators(df):
    # EMA using pandas ewm
    df['ema20'] = df['Close'].ewm(span=EMA_SHORT, adjust=False).mean()
    df['ema50'] = df['Close'].ewm(span=EMA_LONG, adjust=False).mean()

    # Use 'ta' library for indicators
    import ta

    # RSI (14)
    df['rsi14'] = ta.momentum.rsi(df['Close'], window=14, fillna=True)

    # MACD (12,26,9)
    df['macd'] = ta.trend.macd(df['Close'], window_slow=26, window_fast=12, fillna=True)
    df['macd_signal'] = ta.trend.macd_signal(df['Close'], window_slow=26, window_fast=12, window_sign=9, fillna=True)
    df['MACDh_12_26_9'] = df['macd'] - df['macd_signal']

    # ATR (14)
    df['atr14'] = ta.volatility.average_true_range(high=df['High'], low=df['Low'], close=df['Close'], window=14, fillna=True)

    # 20-day avg volume for RVOL
    df['vol20'] = df['Volume'].rolling(window=20, min_periods=10).mean()

    # recent highs/lows
    df['recent_high_10'] = df['High'].rolling(window=10, min_periods=5).max()
    df['recent_low_10'] = df['Low'].rolling(window=10, min_periods=5).min()
    return df
