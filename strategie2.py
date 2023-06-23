from backtesting.lib import crossover
from backtesting import Backtest, Strategy
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import math
# Download historical data for the asset

ticker = "BTC-USD"
data = yf.download(ticker, period="max", start="2016-01-01")
# help(ta.macd)

def StandardDeviation(values):
    mean = pd.Series(values).mean()
    stdDeviation = 0
    stdDeviationNumerator = 0
    somme = 0
    nValues = len(values)
    for value in values:
        if not math.isnan(value):
            stdDeviationNumerator += (value - mean)**2 
        else:
            nValues -= 1
    stdDeviation = math.sqrt(stdDeviationNumerator / nValues)

    return stdDeviation

def ZScore(values):
    mean = pd.Series(values).mean()
    print("Mean: "+ str(mean))
    stdDeviation = StandardDeviation(values)
    print(stdDeviation)
    somme =0
    zscores = []
    for value in values:
            zscores.append((value - mean)/stdDeviation)
    print(pd.Series(zscores))
    return pd.Series(zscores)


class RSItest(Strategy):
    rsi_time = 8
    upper_bound = 70
    lower_bound = 20
    def init(self):
        self.rsi1 = self.I(ta.rsi, pd.Series(self.data.Close),self.rsi_time)
        self.macd1 = self.I(ta.macd, pd.Series(self.data.Close),10,30,10)
        self.zscore = self.I(ZScore, self.data.Close)
        StandardDeviation(self.rsi1)
        ZScore(self.rsi1)
        # print(self.rsi1[5])
    def next(self):
        if crossover( self.rsi1, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi1):
            if not self.position.is_long:
                self.buy()

bt = Backtest(data,RSItest,cash=100_000, commission=0.002)
stats = bt.run()
print(stats)
bt.plot()



