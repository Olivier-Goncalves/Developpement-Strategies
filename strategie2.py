from backtesting.test import GOOG
from backtesting.lib import crossover
from backtesting import Backtest, Strategy
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Download historical data for the asset

ticker = "BTC-USD"
data = yf.download(ticker, period="max", start="2016-01-01")


class RSItest(Strategy):
    def __init__(self):
        self.rsi1 = self.I(data.rsi)
