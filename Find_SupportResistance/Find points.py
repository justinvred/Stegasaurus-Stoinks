import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mplfinance as mpf
from scipy.signal import argrelextrema


import numpy as np
import pandas as pd

text_file = 'C:/Users/pwild/Documents/Projects/Stoinks/6-21-2020 IBM filtered.txt'

def graph_data( text_file ):

    data = pd.read_csv(text_file,index_col=0,parse_dates=[['Date','Time']])
    data.index.name = 'Date'
    data.shape
    data.head(3)
    data.tail(3)

    print(data)

    mpf.plot(data, type='candle', volume=True)
    mpf.plot(data, type='candle')
    # mpf.plot(data, type='line')

def find_points( text_file ):

    data = pd.read_csv(text_file, index_col=0, parse_dates=[['Date', 'Time']])
    data.index.name = 'Date'
    data.shape
    data.head(3)
    data.tail(3)

    print(data)

    points = pd.DataFrame()
    data['min'] = data.Close[(data.Close.shift(1) > data.Close) & (data.Close.shift(-1) > data.Close)]
    data['max'] = data.Close[(data.Close.shift(1) < data.Close) & (data.Close.shift(-1) < data.Close)]

    # filtered the data because the above technique had too many points
    n = 5  # number of points to be checked before and after
    data['minf'] = data.iloc[argrelextrema(data.Close.values, np.less_equal, order=n)[0]]['Close']
    data['maxf'] = data.iloc[argrelextrema(data.Close.values, np.greater_equal, order=n)[0]]['Close']

    # plt.scatter(data.index, data['min'], c='r')
    # plt.scatter(data.index, data['max'], c='r')
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    # ax.plot(data.index, data.Open, color='tab:blue')
    ax.plot(data.index, data.Close, color='tab:orange')
    ax.scatter(data.index, data['minf'], c='r')
    ax.scatter(data.index, data['maxf'], c='r')
    ax.set_title('Plot Open and Close line graphs')
    plt.show()

def find_lines( text_file ):

    data = pd.read_csv(text_file, index_col=0, parse_dates=[['Date', 'Time']])
    data.index.name = 'Date'
    data.shape
    data.head(3)
    data.tail(3)

    print(data)

    n = 8  # number of points to be checked before and after
    data['minf'] = data.iloc[argrelextrema(data.Close.values, np.less_equal, order=n)[0]]['Close']
    data['maxf'] = data.iloc[argrelextrema(data.Close.values, np.greater_equal, order=n)[0]]['Close']

    # converts datatimeindex from pandas to unix time so that it becomes a chronological number = easy to work with
    data['unix'] = data.index.astype(np.int64) // 10**10
    # print(data['unix'])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for index, row in data.iterrows():
        # print(row['minf'])
        # single points to replace Close check with (125.73, 125.26, 122.85, 122.34, 123.22)
        if row['minf'] == 125.73:
            x1 = row['unix']
            y1 = row.Close
            for index2, row2 in data.iterrows():
                if row2['minf'] == row2.Close:
                    x2 = row2['unix']
                    y2 = row2.Close
                    if (x2 > x1):
                        ax.plot([x1,x2], [y1,y2], 'ro-')


    # ax.plot(data.index, data.Open, color='tab:blue')
    ax.plot(data['unix'], data.Close, color='tab:orange')
    ax.scatter(data['unix'], data['minf'], c='r')
    ax.scatter(data['unix'], data['maxf'], c='r')
    ax.set_title('Plot Open and Close line graphs')
    plt.show()

# graph_data(text_file)
# find_points(text_file)
find_lines(text_file)



