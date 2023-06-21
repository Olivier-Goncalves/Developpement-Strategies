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
    # print(stdDeviationNumerator)
    # print("-----------------\nStandard Deviation: " + str(round(stdDeviation,6)))
    # print("Mean: " + str(mean) + "\n-----------------" )
    return stdDeviation

def ZScore(values):
    mean = pd.Series(values).mean()
    print(mean)
    zscores = pd.Series(values)
    stdDeviation = StandardDeviation(values)
    somme =0
    for value in zscores:
        if not math.isnan(value) and somme < 10:
            somme+=1
            print("Valeur brut: " + str(value))
            value = (value - mean)/stdDeviation
            print("Z-Score: " + str(value))
    print("Z-Score 10: "+ str(zscores[10]))
    # print(zscores)
    return zscores


class RSItest(Strategy):
    rsi_time = 8
    upper_bound = 70
    lower_bound = 20
    def init(self):
        self.rsi1 = self.I(ta.rsi, pd.Series(self.data.Close),self.rsi_time)
        self.macd1 = self.I(ta.macd, pd.Series(self.data.Close),10,30,10)
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
# bt.plot()



