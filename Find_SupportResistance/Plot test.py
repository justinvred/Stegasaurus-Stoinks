import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mplfinance as mpf

import numpy as np
import pandas as pd
text_file = 'C:/Users/pwild/Documents/Projects/Stoinks/testdata yestimes.txt'
data = pd.read_csv(text_file,index_col=0,parse_dates=[['Date','Time']])
#data["Dates"] = data["Date"].astype(str) + data["Time"].astype(str)
data.index.name = 'Date'
data.shape
data.head(3)
data.tail(3)

print(data)

mpf.plot(data, type='candle', volume=True)
mpf.plot(data, type='line')