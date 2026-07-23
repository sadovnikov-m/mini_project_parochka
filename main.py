import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from markdown_it.rules_inline import balance_pairs

ticker = "BTC-USD"
raw_data = yf.download(ticker, start="2023-08-28", end="2025-04-06")

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

#Візуалізація
plt.figure(figsize = (10,8))
plt.plot(df['Close'], label='Ціна BTC', color='#4040bf')
plt.plot(df['SMA_short'], label='short SMA', color='#00ff00')
plt.plot(df['SMA_long'], label='long SMA', color='#ff0000')

plt.plot(df[df["Moment"]==1].index,
         df["SMA_short"][df["Moment"]==1],
         "^", markersize=8, color='green', label="Сигнал купівлі")
plt.plot(df[df["Moment"]==-1].index,
         df["SMA_short"][df["Moment"]==-1],
         "^", markersize=8, color='red', label="Сигнал продажу")

plt.title('Торгова стратегія BTC-USD')
plt.xlabel("ДАТА")
plt.ylabel("ЦІНА (USD)")
plt.legend()
plt.grid(True)
plt.show()