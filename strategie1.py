from backtesting.test import GOOG
from backtesting.lib import crossover
from backtesting import Backtest, Strategy
import pandas as pd
import yfinance as yf

# Download historical data for the asset

ticker = "BTC-USD"
data = yf.download(ticker, period="max", start="2017-01-01")

def SMA (values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


class DoubleSMA(Strategy):
    n1= 200
    # n2 = 730
    
    def init(self):
        # testData = self.data.Close * 2
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        # self.sma2 = self.I(SMA, self.data.Close * 5, self.n2)
        # print(self.sma2)
    def next(self):
        if crossover(self.sma1, self.data.Close):
            self.position.close()
            self.buy()
        elif crossover(self.data.Close, self.sma1):
            self.position.close()
            self.sell()

bt = Backtest(data, DoubleSMA, cash=100_000, commission=0.002)
stats = bt.run()
bt.plot()
print(stats)

