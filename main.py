import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker = "BTC-USD"
raw_data = yf.download(ticker, start="2023-08-28", end="2026-04-06")

df=pd.DataFrame(raw_data)

#Перевірка даних
#print(df.isnull().sum())
df=df.dropna()
print(df)
