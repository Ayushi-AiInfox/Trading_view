import yfinance as yf
import pandas as pd

# Fetch OHLCV data for a specific stock (e.g., Apple Inc.)
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2024-12-11", interval="1d")
data = data.drop(columns=('Adj Close',ticker))
data.columns = [col[0] for col in data.columns]
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA



class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()
bt = Backtest(data, SmaCross, commission=.002,
              exclusive_orders=True,cash=10000000)
stats = bt.run()
print(stats)