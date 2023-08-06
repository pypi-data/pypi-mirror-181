from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.dont_write_bytecode = True

import backtrader as bt
import pandas as pd

feed = bt.feed.CSVData(
	files=[
		"/Users/pol.maksim/Downloads/OHLC Data/binance/futures/BTCUSDT-2021-1m.csv",
		"/Users/pol.maksim/Downloads/OHLC Data/binance/futures/BTCUSDT-2022-1m.csv"
	],
	timestamp=0,
	datetime=1,
	open=3,
	high=4,
	low=5,
	close=6,
	volume=7,
	dtformat="%Y-%m-%d %H:%M:%S",
	separator=",",
	header=1,
	start_date=pd.Timestamp(year=2017, month=1, day=1),
	# end_date=pd.Timestamp(year=2017, month=12, day=31)
)

df = feed.load()

class BuyAndHold24Hours(bt.Strategy):
	def __init__(self):
		super().__init__()

		self.min_trade_notional = 10
		self.max_balance_risk = 0.1

	def next(self):
		if self.data.datetime.hour == 0 and self.data.datetime.minute == 0:
			notional = self.broker.cash * self.max_balance_risk

			if notional >= self.min_trade_notional:
				qty = notional / self.data.close
				self.buy(quantity=qty)
		elif self.data.datetime.hour == 23 and self.data.datetime.minute == 59:
			if self.position is not None:
				self.sell(quantity=self.position.size, reduce_only=True)

strategy = BuyAndHold24Hours()
strategy.set_debug_mode(False)
strategy.set_maker_fee_rate(0.02)
strategy.set_taker_fee_rate(0.04)
strategy.set_funding_rate(0.01)
strategy.set_base_precision(8)
strategy.set_quote_precision(2)
strategy.set_price_precision(2)
strategy.set_cash(10000)
strategy.set_data(df)

report = strategy.run()

report.plot()
