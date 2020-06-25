import matplotlib.pyplot as plt
import numpy as np
import urllib
import matplotlib.dates as mdates
import mplfinance as mpf

def graph_data():

    date, time, openp, highp, lowp, closep, volume = np.genfromtxt('C:/Users/pwild/Documents/Projects/Stoinks/testdata.txt',
                                                                delimiter=',',
                                                                names=True,
                                                                dtype=None)

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(append_me)
        x += 1
    print(ohlc)
    # mpf.plot(ohlc)

graph_data()