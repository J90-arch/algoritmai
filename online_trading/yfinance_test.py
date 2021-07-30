import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr

FEATURE_COLUMNS = ['open', 'high', 'low', 'close', 'volume']
#yf.pdr_override()
#df = pdr.get_data_yahoo(tickers='AAPL', period='15m', interval='1m')
df = yf.Ticker('AAPL').history(period='15m', interval='1m')[['Open', 'High', 'Low', 'Close', 'Volume']]
df.index = df.index.tz_localize(None)
df.columns = FEATURE_COLUMNS
df.to_csv('tmp.csv')
with open('tmp.csv', 'r', encoding='utf-8') as F:
    tmp_df = F.readlines()
tmp_df[0] = tmp_df[0][8:]
print(tmp_df)
with open('tmp.csv', 'w', encoding='utf-8') as F:
    F.writelines(tmp_df)
df = pd.read_csv('tmp.csv')
print(df)