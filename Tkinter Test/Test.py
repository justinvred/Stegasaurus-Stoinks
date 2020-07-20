import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from scipy.signal import argrelextrema
#from scipy import signal
import os
import threading
from time import sleep
import urllib
import json

#Alpha Vantage api code
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='H9NR2L5ZM2CVKP9W', output_format='pandas')


#alpaca api code
import alpaca_trade_api as tradeapi
api = tradeapi.REST("PKE979F3JHG3KU3OXWGY", "UeXXV2hxsjkea1wFkEP4IMPY3LX70uxFF1fba0Gl")
#barset = api.get_barset('AAPL', 'day', limit=5)
#appl_bars = barset['AAPL']
#print(appl_bars)

aapl = pd.DataFrame(columns=['date', '1. open', '2. high', '3. low', '4. close', '5. volume'])

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = Figure()
a = f.add_subplot(111)

text_file = '6-16-20_IBM.txt'

TickerList = ["SPY"]

data = pd.read_csv(text_file,index_col=0,parse_dates=[['Date','Time']])
data.index.name = 'Date'
data.shape
data.head(3)
data.tail(3)

exchange = "EXCHANGE 1"
DatCounter = 9000
programName = "exchange1"

resampleSize = "15Min"
dataPace = "1d"
candleWidth = 0.008
topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
EMAs = []
SMAs = []


def addTopIndicator(what):
    global topIndicator
    global DatCounter

    if what == "none":
        topIndicator = what
        DatCounter = 9000

    elif what == "rsi":

        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global topIndicator
            global DatCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            topIndicator = group
            DatCounter = 9000
            print("Set top indicator to",group)
            rsiQ.destroy()

        b=ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":

        topIndicator = "macd"
        DatCounter = 9000


def addBottomIndicator(what):
    global bottomIndicator
    global DatCounter

    if what == "none":
        bottomIndicator = what
        DatCounter = 9000

    elif what == "rsi":

        rsiQ = tk.Tk()
        rsiQ.wm_title("Periods?")
        label = ttk.Label(rsiQ, text = "Choose how many periods you want each RSI calculation to consider.")
        label.pack(side="top", fill="x", pady=10)

        e = ttk.Entry(rsiQ)
        e.insert(0,14)
        e.pack()
        e.focus_set()

        def callback():
            global bottomIndicator
            global DatCounter

            periods = (e.get())
            group = []
            group.append("rsi")
            group.append(periods)

            bottomIndicator = group
            DatCounter = 9000
            print("Set bottom indicator to",group)
            rsiQ.destroy()

        b=ttk.Button(rsiQ, text="Submit", width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif what == "macd":

        bottomIndicator = "macd"
        DatCounter = 9000


def addMiddleIndicator(what):
    global middleIndicator
    global DatCounter

    if what != "none":
        if middleIndicator == "none":
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0,10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to:",middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to:", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

        else:
            if what == "sma":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    #middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("sma")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to:", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

            if what == "ema":
                midIQ = tk.Tk()
                midIQ.wm_title("Periods?")
                label = ttk.Label(midIQ, text="Choose how many periods you want")
                label.pack(side="top", fill="x", pady=10)
                e = ttk.Entry(midIQ)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global middleIndicator
                    global DatCounter

                    #middleIndicator = []
                    periods = (e.get())
                    group = []
                    group.append("ema")
                    group.append(int(periods))
                    middleIndicator.append(group)
                    DatCounter = 9000
                    print("middle indicator set to:", middleIndicator)
                    midIQ.destroy()

                b = ttk.Button(midIQ, text="Submit", width=10, command=callback)
                b.pack()
                tk.mainloop()

    else:
        middleIndicator = "none"


def changeTimeFrame(tf):
    global dataPace
    global DatCounter

    dataPace = tf
    DatCounter = 9000


def changeSampleSize(size, width):
    global resampleSize
    global DatCounter
    global candleWidth

    resampleSize = size
    DatCounter = 9000
    candleWidth = width


def ShutProgram():
    print("Quitting Program")
    app.destroy()


def changeExchange(toWhat, pn):
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000


def popupmsg(msg):
    popup = tk.Tk()

    def leavemini():
        popup.destroy()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = leavemini)
    B1.pack()
    popup.mainloop()


def simLiveData():
    global aapl
    #alpaca
    #aapl = api.alpha_vantage.intraday_quotes('AAPL', interval="5min", outputsize='day', output_format='pandas')
    #alphavantage
    aapl, meta_data = ts.get_intraday(symbol='IBM', interval='1min', outputsize='full')
    print(aapl)
    print("Data Added")
    return aapl


def animate(i):
    global aapl
    #print(aapl)
    pullData = open("TestData.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))

    a.clear()


    last_index = len(aapl.index) - 1
    if last_index >= 0:
        title = "AAPL Prices\nLast Price: "+str(aapl['4. close'][last_index])
        aapl['Day'] = aapl.index.day
        current_day = aapl.iloc[0]['Day']
        print(current_day)

        aapl_day = aapl[aapl['Day'] == current_day]

        n = 4 # number of points to check before and after current point
        #aapl_day['minf'] = data.iloc[signal.argrelextrema(aapl_day['4. close'].values, np.less_equal, order=n)[0]]['4. close']
        #aapl_day['maxf'] = data.iloc[signal.argrelextrema(aapl_day['4. close'].values, np.greater_equal, order=n)[0]]['4. close']

        #a.scatter(aapl_day.index, data['minf'], c='r')
        #a.scatter(aapl_day.index, data['maxf'], c='r')
        a.plot_date(aapl_day.index, aapl_day['4. close'], "#00A3E0", label="Close")
        a.plot_date(aapl_day.index, aapl_day['1. open'], "r", label="Open")

        a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
                 ncol=2, borderaxespad=0)

    else:
        title = "AAPL Prices\nLast Price: N/A"

    a.set_title(title)
    # a.plot(xList, yList)



class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="Stonks_Guy.ico")
        tk.Tk.wm_title(self, "Stonks Up")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = "True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command = ShutProgram)
        menubar.add_cascade(label="File", menu=filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff = 1)
        exchangeChoice.add_command(label="EXCHANGE NAME 1",
                                   command=lambda: changeExchange("DISPLAY_NAME 1","BACKEND_NAME"))
        exchangeChoice.add_command(label="EXCHANGE NAME 2",
                                   command=lambda: changeExchange("DISPLAY_NAME 2", "BACKEND_NAME"))
        exchangeChoice.add_command(label="EXCHANGE NAME 3",
                                   command=lambda: changeExchange("DISPLAY_NAME 3", "BACKEND_NAME"))
        exchangeChoice.add_command(label="EXCHANGE NAME 4",
                                   command=lambda: changeExchange("DISPLAY_NAME 4", "BACKEND_NAME"))

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)

        dataTF = tk.Menu(menubar, tearoff = 1)
        dataTF.add_command(label="1 Hour",
                           command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label="3 Hour",
                           command=lambda: changeTimeFrame('tick'))
        dataTF.add_command(label="1 Day",
                           command=lambda: changeTimeFrame('1d'))
        dataTF.add_command(label="3 Day",
                           command=lambda: changeTimeFrame('3d'))
        dataTF.add_command(label="1 Week",
                           command=lambda: changeTimeFrame('7d'))
        dataTF.add_command(label="1 Month",
                           command=lambda: changeTimeFrame('30d'))
        dataTF.add_command(label="3 Month",
                           command=lambda: changeTimeFrame('90d'))
        menubar.add_cascade(label="Data Time Frame", menu=dataTF)

        OHLCI = tk.Menu(menubar, tearoff=1)

        OHLCI.add_command(label="1 minute",
                          command=lambda: changeSampleSize('1Min',0.0005))
        OHLCI.add_command(label="5 minute",
                          command=lambda: changeSampleSize('5Min', 0.003))
        OHLCI.add_command(label="15 minute",
                          command=lambda: changeSampleSize('15Min', 0.008))
        OHLCI.add_command(label="30 minute",
                          command=lambda: changeSampleSize('30Min', 0.016))
        OHLCI.add_command(label="1 Hour",
                          command=lambda: changeSampleSize('1H', 0.032))
        OHLCI.add_command(label="1 Day",
                          command=lambda: changeSampleSize('1D', 0.096))

        menubar.add_cascade(label="OHCL Interval", menu=OHLCI)

        topIndi = tk.Menu(menubar, tearoff=1)
        topIndi.add_command(label="None",
                            command = lambda: addTopIndicator("none"))
        topIndi.add_command(label="RSI",
                            command=lambda: addTopIndicator("rsi"))
        topIndi.add_command(label="MACD",
                            command=lambda: addTopIndicator("macd"))
        topIndi.add_command(label="VWAP",
                            command=lambda: addTopIndicator("vwap"))
        menubar.add_cascade(label="Top Indicator", menu=topIndi)


        mainIndi = tk.Menu(menubar, tearoff=1)
        mainIndi.add_command(label="None",
                            command=lambda: addMiddleIndicator("none"))
        mainIndi.add_command(label="SMA",
                            command=lambda: addMiddleIndicator("sma"))
        mainIndi.add_command(label="EMA",
                            command=lambda: addMiddleIndicator("ema"))

        menubar.add_cascade(label="Main/Middle Indicator", menu=mainIndi)

        bottomIndi = tk.Menu(menubar, tearoff=1)
        bottomIndi.add_command(label="None",
                            command=lambda: addBottomIndicator("none"))
        bottomIndi.add_command(label="RSI",
                            command=lambda: addBottomIndicator("rsi"))
        bottomIndi.add_command(label="MACD",
                            command=lambda: addBottomIndicator("macd"))
        bottomIndi.add_command(label="VWAP",
                            command=lambda: addBottomIndicator("vwap"))

        menubar.add_cascade(label="Bottom Indicator", menu=bottomIndi)


        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, Opt_HomePage, BackTestPage, LivePlotting):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="""ALPHA Trading Platform for multiple exchanges,
         
USE AT YOUR OWN RISK""",font=LARGE_FONT)

        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                             command=lambda: controller.show_frame(Opt_HomePage))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                             command=ShutProgram)
        button2.pack()


class Opt_HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Options Trading HomePage!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Live Trading",
                             command=lambda: controller.show_frame(LivePlotting))
        button2.pack()

        button3 = ttk.Button(self, text="Backtesting and Development",
                             command=lambda: controller.show_frame(BackTestPage))
        button3.pack()

        button4 = ttk.Button(self, text="Quit",
                             command=lambda: ShutProgram())
        button4.pack()


class BackTestPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BackTesting and Development", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(Opt_HomePage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        update_button = ttk.Button(self, text="Update",
                             command=lambda: simLiveData())
        update_button.pack()


class LivePlotting(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Live Trading", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command = lambda: controller.show_frame(Opt_HomePage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        update_button = ttk.Button(self, text="Update",
                             command=lambda: simLiveData())
        update_button.pack()


app = SeaofBTCapp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
