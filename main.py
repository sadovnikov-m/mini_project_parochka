import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from markdown_it.rules_inline import balance_pairs

ticker = "BTC-USD"
raw_data = yf.download(ticker, start="2023-08-28", end="2026-04-06")

df=pd.DataFrame(raw_data)

#Перевірка даних
#print(df.isnull().sum())
df=df.dropna()

# Розробка базової моделі торгівлі на основі простої стратегії.
short_window=30
long_window=60

df['SMA_short']=df['Close'].rolling(window=short_window).mean()
df['SMA_long']=df['Close'].rolling(window=long_window).mean()

df['Signal']=0.0
df['Signal']=np.where(df['SMA_short']>df['SMA_long'],1.0,0.0)
df['Moment']=df['Signal'].diff()
df=df.dropna()
# print(df['Signal'])
# print(df['Moment'])
#Сигнали: 1.0 - точка купівлі, -1.0 - точка продажу

#Розрахуйте прибуток/збиток (P&L)
balance = 0.0
buy_price = 0.0
in_position = False
for i in range(len(df)):
    current_price = float(df['Close'].iloc[i].item())
    moment = float(df['Moment'].iloc[i].item())
    if moment == 1.0 and not in_position:
        buy_price = current_price
        in_position = True
    elif moment == -1.0 and in_position:
        sell_price = current_price
        trade_profit = sell_price - buy_price
        balance += trade_profit
        in_position = False
print(f"Загальний прибуток: {balance:.2f}$")



