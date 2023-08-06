from __future__ import (absolute_import, division, print_function, unicode_literals)

class Config:
	def __init__(self):
		self.__debug = False
		self.__maker_fee_rate = 0.0005
		self.__taker_fee_rate = 0.001
		self.__funding_rate = 0.0001
		self.__funding_rate_hours = [0, 8, 16]
		self.__leverage = 1
		self.__base_precision = 8
		self.__quote_precision = 2
		self.__price_precision = 2

	@property
	def debug(self) -> bool:
		return self.__debug

	@debug.setter
	def debug(self, value: bool):
		self.__debug = value

	@property
	def maker_fee_rate(self) -> float:
		return self.__maker_fee_rate

	@maker_fee_rate.setter
	def maker_fee_rate(self, value: float):
		self.__maker_fee_rate = value

	@property
	def taker_fee_rate(self) -> float:
		return self.__taker_fee_rate

	@taker_fee_rate.setter
	def taker_fee_rate(self, value: float):
		self.__taker_fee_rate = value

	@property
	def funding_rate(self) -> float:
		return self.__funding_rate

	@funding_rate.setter
	def funding_rate(self, value: float):
		self.__funding_rate = value

	@property
	def funding_rate_hours(self) -> list[int]:
		return self.__funding_rate_hours

	@funding_rate_hours.setter
	def funding_rate_hours(self, hours: list[int]):
		self.__funding_rate_hours = hours

	@property
	def leverage(self) -> int:
		return self.__leverage

	@leverage.setter
	def leverage(self, value: int):
		self.__leverage = value

	@property
	def base_precision(self) -> int:
		return self.__base_precision

	@base_precision.setter
	def base_precision(self, value: int):
		self.__base_precision = value

	@property
	def quote_precision(self) -> int:
		return self.__quote_precision

	@quote_precision.setter
	def quote_precision(self, value: int):
		self.__quote_precision = value

	@property
	def price_precision(self) -> int:
		return self.__price_precision

	@price_precision.setter
	def price_precision(self, value: int):
		self.__price_precision = value
