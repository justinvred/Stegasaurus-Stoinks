import plotly.graph_objects as ply
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import os

# from matplotlib.finance import candlestick_ohlc
from mpl_finance import candlestick_ohlc

from matplotlib.pyplot import figure

path = "C:/Users/pwild/Documents/Projects/Stoinks/"

file_name = os.path.join(path, "6-21-2020 IBM.txt")
my_file = open(file_name)
ticker_data = my_file.read()

cpb_mpl = ticker_data
# print(ticker_data)

# Convert Date column to Matplotlib's float format
import matplotlib.dates as dates
cpb_mpl.Date = dates.datestr2num(cpb_mpl.Date)

# Create a list of lists where each inner-list represents
# one day's trading history
cpb_subset = cpb_mpl[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
cpb_list = [list(x) for x in cpb_subset.values]

# Build the plot
fig = plt.figure(figsize=(16,8))
ax1 = plt.subplot2grid((1,1), (0,0))

candlestick_ohlc(ax1, cpb_list, width=0.4, colorup='#77d879', colordown='#db3f3f')

for label in ax1.xaxis.get_ticklabels():
     label.set_rotation(45)

ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax1.grid(True)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Campbell Soup Company')
plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
plt.show()

# fig = ply.Figure(data=ply.Bar(y=[2, 3, 1]))
# fig.show()