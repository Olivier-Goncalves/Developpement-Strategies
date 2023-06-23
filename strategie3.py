import pandas as pd
import pandas_ta as ta
from backtesting.lib import crossover
from backtesting import Backtest, Strategy
import yfinance as yf
import math

ticker = "BTC-USD"
data = yf.download(ticker, period="max", start="2016-01-01")
class ADXsimple(Strategy):
    lenght = 14
    def init(self):
        self.adx = self.I(ta.adx,pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close))
        self.adx.title = "test"
    def next(self):
        if(self.adx > 50):
            self.buy()
        elif(self.adx < 20):
            self.position.close
        elif(self.adx > 75):
            self.position.close

bt = Backtest(data, ADXsimple,cash=100_000, commission=0.002)
stats = bt.run()

print(stats)

bt.plot()