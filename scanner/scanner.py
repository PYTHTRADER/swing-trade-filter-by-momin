import yfinance as yf
import pandas_ta as ta
import pandas as pd, numpy as np, json, time
from datetime import datetime, timedelta

TICKERS = ['TCS.NS','HDFCBANK.NS','RELIANCE.NS','IRCTC.NS','BEL.NS','CAMS.NS','TATAMOTORS.NS','COFORGE.NS','IRFC.NS']
LOOKBACK_DAYS = 90
RVOL_THRESHOLD = 1.8
RSI_BUY = 55

def fetch(ticker):
    end=datetime.now(); start=end-timedelta(days=LOOKBACK_DAYS)
    df=yf.download(ticker,start=start,end=end,progress=False)
    if df.empty: return None
    df['rsi']=ta.rsi(df['Close'],14)
    df['ema20']=ta.ema(df['Close'],20)
    df['vol20']=df['Volume'].rolling(20).mean()
    df['recent_high']=df['High'].rolling(10).max()
    last=df.iloc[-1]
    rvol=last['Volume']/last['vol20']
    if last['Close']>last['recent_high'] and last['rsi']>RSI_BUY and rvol>RVOL_THRESHOLD:
        return {'ticker':ticker.replace('.NS',''),'price':round(last['Close'],2),'rsi':round(last['rsi'],2),'rvol':round(rvol,2)}
    return None

res=[]
for t in TICKERS:
    try:
        sig=fetch(t)
        if sig: res.append(sig)
        time.sleep(0.5)
    except: pass

with open("signals.json","w") as f:
    json.dump({'date':datetime.utcnow().isoformat(),'signals':res},f,indent=2)
print("Saved",len(res),"signals")
