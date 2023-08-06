from __future__ import (absolute_import, division, print_function, unicode_literals)
import pandas as pd
from .config import *
from .store import *
from .broker import *
from .position import *

class Backtrader:
	def __init__(self):
		self.__cfg = Config()
		self.__store = Store()
		self.__broker = Broker()

	@property
	def cfg(self) -> Config:
		return self.__cfg

	@property
	def store(self) -> Store:
		return self.__store

	@property
	def broker(self) -> Broker:
		return self.__broker

	def set_debug_mode(self, enabled: bool):
		self.__cfg.debug = enabled

	def set_maker_fee_rate(self, percent: float):
		self.__cfg.maker_fee_rate = percent / 100

	def set_taker_fee_rate(self, percent: float):
		self.__cfg.taker_fee_rate = percent / 100

	def set_cash(self, amount: float):
		self.__broker = Broker(start_cash=amount)

	def set_funding_rate(self, percent: float):
		self.__cfg.funding_rate = percent / 100

	def set_funding_rate_hours(self, hours: list[int]):
		self.__cfg.funding_rate_hours = hours

	def set_leverage(self, leverage: int):
		self.__cfg.leverage = leverage

	def set_base_precision(self, precision: int):
		self.__cfg.base_precision = precision

	def set_quote_precision(self, precision: int):
		self.__cfg.quote_precision = precision

	def set_price_precision(self, precision: int):
		self.__cfg.price_precision = precision

	def set_data(self, data: pd.DataFrame):
		self.__store.raw_data = data.reset_index().rename(columns={"index": "datetime"})
