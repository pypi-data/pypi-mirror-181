from __future__ import (absolute_import, division, print_function, unicode_literals)
import pandas as pd
from .reference import *
from . import utils

class Position:
	def __init__(self, side: str, price: float, size: float, created_at: pd.Timestamp, leverage: int = 1):
		self.__side = side
		self.__avg_price = price
		self.__size = size
		self.__created_at = created_at
		self.__leverage = leverage

	def _increase(self, price: float, size: float):
		self.__avg_price = (self.notional + (price * size)) / (self.__size + size)
		self.__size += size

	def _decrease(self, size: float):
		self.__size -= size

	@property
	def side(self) -> str:
		return self.__side

	@property
	def avg_price(self) -> float:
		return self.__avg_price

	@property
	def size(self) -> float:
		return self.__size

	@property
	def created_at(self) -> pd.Timestamp:
		return self.__created_at

	@property
	def leverage(self) -> int:
		return self.__leverage

	@property
	def notional(self) -> float:
		return self.__avg_price * self.__size

	@property
	def margin(self) -> float:
		return self.notional * (1 / self.__leverage)

	@property
	def liquidation_price(self) -> float:
		return utils.get_liquidation_price(self.__side, self.__avg_price, self.__leverage)

	def get_breakeven_price(self, fee_rate: float) -> float:
		return utils.get_breakeven_price(self.__side, self.__avg_price, self.__size, fee_rate)

	def get_unrealized_pnl(self, price: float) -> float:
		if self.__side == POSITION_SIDE_LONG:
			return (price - self.__avg_price) * self.__size
		elif self.__side == POSITION_SIDE_SHORT:
			return (self.__avg_price - price) * self.__size
		else:
			raise Exception("Unknown position side.")
