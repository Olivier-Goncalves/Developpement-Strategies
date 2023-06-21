from backtesting.test import GOOG
from backtesting.lib import crossover
from backtesting import Backtest, Strategy
import pandas as pd
import yfinance as yf

# Download historical data for the asset

ticker = "BTC-USD"
data = yf.download(ticker, period="max", start="2016-01-01")


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values
    """
    return pd.Series(values).rolling(n).mean()


def optim_func(series):
    if series["# Trades"] < 10:
        return -1
    else:
        return "Return [%]"


class DoubleSMA(Strategy):
    n1 = 700
    multiplicateurSma2 = 5

    def init(self):
        # testData = self.data.Close * 2
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(
            SMA, self.data.Close * self.multiplicateurSma2 * 0.1, self.n1
        )
        # print(self.sma2)

    def next(self):
        if crossover(self.sma1, self.data.Close) or crossover(
            self.data.Close, self.sma1
        ):
            if not self.position.is_long:
                self.position.close()
                self.buy()

        elif crossover(self.data.Close, self.sma2) or crossover(
            self.sma2, self.data.Close
        ):
            if not self.position.is_short:
                self.position.close()
                # self.sell()


bt = Backtest(data, DoubleSMA, cash=100_000, commission=0.002)
stats = bt.optimize(n1=range(50, 700, 20), multiplicateurSma2=range(20, 70, 5))
bt.plot()
print(stats)
