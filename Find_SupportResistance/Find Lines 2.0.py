import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import mplfinance as mpf
from scipy.signal import argrelextrema


import numpy as np
import pandas as pd

text_file = 'C:/Users/pwild/Documents/Projects/Stoinks/6-16-2020 IBM filtered.txt'
# 6-16-2020 IBM filtered

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
    n = 4  # number of points to be checked before and after
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

    # print(data)

    valley_points = pd.DataFrame(columns=['x', 'y'])
    peak_points = pd.DataFrame(columns=['x', 'y'])

    n = 4  # number of points to be checked before and after
    data['minf'] = data.iloc[argrelextrema(data.Close.values, np.less_equal, order=n)[0]]['Close']
    data['maxf'] = data.iloc[argrelextrema(data.Close.values, np.greater_equal, order=n)[0]]['Close']

    # converts datatimeindex from pandas to unix time so that it becomes a chronological number = easy to work with
    data['unix'] = data.index.astype(np.int64) // 10**10
    # print(data['unix'])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for index, row in data.iterrows():
        # print(row['minf'])

        if row['maxf'] == row.Close:
            new_point = {'x': row['unix'], 'y': row['maxf']}
            peak_points = peak_points.append(new_point, ignore_index=True)

        if row['minf'] == row.Close:
            new_point = {'x': row['unix'], 'y': row['minf']}
            valley_points = valley_points.append(new_point, ignore_index=True)

    # print(valley_points)
    # find lines between points that are valid
    for index, point1 in valley_points.iterrows():
        # print(row['minf'])
        # single points to replace Close check with (125.73, 125.26, 122.85, 122.34, 123.22)
        x1 = point1['x']
        y1 = point1['y']
        for index2, point2 in valley_points.iterrows():
            x2 = point2['x']
            y2 = point2['y']

            if x2 > x1:

                slope = (y2-y1)/(x2-x1)
                intercept = y2-(slope*x2)
                # print(slope, intercept)

                valid = True

                b = (valley_points.loc[((valley_points['x'] > x1) & (valley_points['x'] < x2))])

                # idk if this is a solution
                if len(b.index) < 1:
                    valid = False

                for ind, midpoint in b.iterrows():
                    if midpoint['y'] < ((slope*midpoint['x'])+intercept):
                        valid = False

                if valid:
                    ax.plot([x1, x2], [y1, y2], 'ro-')

    # repeat above for peak points
    for index, point1 in peak_points.iterrows():
        # print(row['maxf'])
        x1 = point1['x']
        y1 = point1['y']
        for index2, point2 in peak_points.iterrows():
            x2 = point2['x']
            y2 = point2['y']

            if x2 > x1:

                slope = (y2-y1)/(x2-x1)
                intercept = y2-(slope*x2)
                # print(slope, intercept)

                valid = True

                b = (peak_points.loc[((peak_points['x'] > x1) & (peak_points['x'] < x2))])

                #idk if this is a solution
                if len(b.index) < 1:
                    valid = False

                for ind, midpoint in b.iterrows():
                    if midpoint['y'] > ((slope*midpoint['x'])+intercept):
                        valid = False

                if valid:
                    ax.plot([x1, x2], [y1, y2], 'bo-')



    # ax.plot(data.index, data.Open, color='tab:blue')
    ax.plot(data['unix'], data.Close, color='tab:orange')
    ax.scatter(valley_points['x'], valley_points['y'], c='r')
    ax.scatter(peak_points['x'], peak_points['y'], c='b')
    ax.set_title('Support (Red) and Resistance (Blue) Lines')
    plt.show()

# graph_data(text_file)
# find_points(text_file)
find_lines(text_file)



