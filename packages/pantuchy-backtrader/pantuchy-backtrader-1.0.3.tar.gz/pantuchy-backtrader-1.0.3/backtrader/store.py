from __future__ import (absolute_import, division, print_function, unicode_literals)
import pandas as pd
from .reference import *

class Store:
	def __init__(self):
		self.__raw_data = None
		self.__portfolio_history = []
		self.__transaction_history = []
		self.__trade_history = []

	@property
	def raw_data(self) -> pd.DataFrame:
		return self.__raw_data

	@raw_data.setter
	def raw_data(self, data: pd.DataFrame):
		self.__raw_data = data

	@property
	def transactions(self) -> list:
		return self.__transaction_history

	def _add_transaction(self, row: list):
		self.__transaction_history.append(row)

	@property
	def trades(self) -> list:
		return self.__trade_history

	def _add_trade(self, row: list):
		self.__trade_history.append(row)

	@property
	def portfolio_history(self) -> list:
		return self.__portfolio_history

	def _add_portfolio_history(self, row: list):
		if row[0].hour == 0 and row[0].minute == 0:
			self.__portfolio_history.append(row)
