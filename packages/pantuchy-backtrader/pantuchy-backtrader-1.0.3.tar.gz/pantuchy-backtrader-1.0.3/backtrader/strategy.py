from __future__ import (absolute_import, division, print_function, unicode_literals)
from typing import final
import math
import datetime as dt
from datetime import timezone
from .backtrader import *
from .position import *
from .reference import *
from .report import *

class Strategy(Backtrader):
	def __init__(self):
		super().__init__()
		self.__data = None
		self.__position = None
		self.__logs = []

	@final
	def __ohlc_log(self) -> str:
		msg = f"Open: {self.__data.open:.{self.cfg.price_precision}f}, "
		msg += f"High: {self.__data.high:.{self.cfg.price_precision}f}, "
		msg += f"Low: {self.__data.low:.{self.cfg.price_precision}f}, "
		msg += f"Close: {self.__data.close:.{self.cfg.price_precision}f}"
		return msg

	@final
	def __trade_log(self, side: str, quantity: float, price: float, notional: float, fee: float) -> str:
		msg = f"{side} quantity of {quantity:.{self.cfg.base_precision}f} "
		msg += f"at price {price:.{self.cfg.price_precision}f}, "
		msg += f"notional {notional:.{self.cfg.quote_precision}f} "
		msg += f"and fee {fee:.{self.cfg.quote_precision}f}"
		return msg

	@final
	def __reduced_position_log(self, quantity: float, margin: float) -> str:
		msg = f"Reduced {self.__position.side} position "
		msg += f"by size {quantity:.{self.cfg.base_precision}f} and "
		msg += f"margin by {margin:.{self.cfg.quote_precision}f}"
		return msg

	@final
	def __increased_position_log(self, quantity: float, margin: float) -> str:
		msg = f"Increased {self.__position.side} position "
		msg += f"by size {quantity:.{self.cfg.base_precision}f} and "
		msg += f"margin by {margin:.{self.cfg.quote_precision}f}"
		return msg

	@final
	def __opened_position_log(self) -> str:
		msg = f"Opened {self.__position.side} position "
		msg += f"with size {self.__position.size:.{self.cfg.base_precision}f}, "
		msg += f"margin {self.__position.margin:.{self.cfg.quote_precision}f} "
		msg += f"and leverage {self.__position.leverage}"
		return msg

	@final
	def __closed_position_log(self) -> str:
		msg = f"Closed {self.__position.side} position "
		msg += f"with size {self.__position.size:.{self.cfg.base_precision}f}, "
		msg += f"margin {self.__position.margin:.{self.cfg.quote_precision}f} "
		msg += f"and leverage {self.__position.leverage}"
		return msg

	@final
	def __current_position_log(self) -> str:
		msg = f"Current {self.__position.side} position "
		msg += f"size {self.__position.size:.{self.cfg.base_precision}f}, "
		msg += f"margin {self.__position.margin:.{self.cfg.quote_precision}f} "
		msg += f"and leverage {self.__position.leverage}"
		return msg

	@final
	def __print_logs(self):
		if len(self.__logs) > 0:
			ts = self.__data.datetime.strftime("%Y-%m-%d %H:%M:%S")
			msg = ""

			for log in self.__logs:
				msg += " - " + log + "\n"

			print(f"{ts}\n{msg}")

	@final
	def __buy(self, quantity: float, price: float, reduce_only: bool = False, is_maker: bool = False):
		if math.isnan(price) or price <= 0:
			raise Exception("Price must be greater zero.")

		if math.isnan(quantity) or quantity <= 0:
			raise Exception("Quantity must be greater zero.")

		fee_rate = self.cfg.maker_fee_rate if is_maker else self.cfg.taker_fee_rate
		self.__logs.append(self.__ohlc_log())
		self.__logs.append(f"Cash before {self.broker.cash:.{self.cfg.quote_precision}f}")

		if reduce_only:
			if self.__position is not None:
				if self.__position.side != POSITION_SIDE_SHORT:
					raise Exception(f"Wrong order side to reduce {self.__position.side} position.")

				rqty = quantity

				if quantity > self.__position.size:
					rqty = self.__position.size

				pnl = (self.__position.avg_price - price) * rqty
				notional = price * rqty
				fee = notional * fee_rate
				margin = (self.__position.avg_price * rqty) * (1 / self.__position.leverage)
				self.broker._add_cash(margin + pnl - fee)
				self.__position._decrease(rqty)
				self.store._add_trade([self.__data.datetime, ORDER_SIDE_BUY, rqty, price, notional, fee, pnl])
				self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_REALIZED_PNL, pnl])
				self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_COMMISSION, fee * -1])
				self.__logs.append(self.__trade_log(side=ORDER_SIDE_BUY, quantity=rqty, price=price, notional=notional, fee=fee))

				if self.__position.size > 0:
					self.__logs.append(self.__reduced_position_log(quantity=rqty, margin=margin))
					self.__logs.append(self.__current_position_log())
				else:
					self.__logs.append(self.__closed_position_log())
					self.__position = None

				self.__logs.append(f"Realized PNL {pnl:.{self.cfg.quote_precision}f}")
				self.__logs.append(f"Cash after {self.broker.cash:.{self.cfg.quote_precision}f}")
			else:
				raise Exception("No opened positions to reduce size.")
		else:
			notional = price * quantity
			fee = notional * fee_rate

			if self.__position is not None:
				margin = notional * (1 / self.__position.leverage)

				if self.broker.cash < margin + fee:
					raise Exception("Insufficient funds.")

				self.__position._increase(price, quantity)
				self.broker._sub_cash(margin + fee)
				self.__logs.append(self.__trade_log(side=ORDER_SIDE_BUY, quantity=quantity, price=price, notional=notional, fee=fee))
				self.__logs.append(self.__increased_position_log(quantity=quantity, margin=margin))
				self.__logs.append(self.__current_position_log())
			else:
				margin = notional * (1 / self.cfg.leverage)

				if self.broker.cash < margin + fee:
					raise Exception("Insufficient funds.")

				self.__position = Position(
					side=POSITION_SIDE_LONG,
					price=price,
					size=quantity,
					created_at=self.__data.datetime,
					leverage=self.cfg.leverage
				)

				self.broker._sub_cash(margin + fee)
				self.__logs.append(self.__trade_log(side=ORDER_SIDE_BUY, quantity=quantity, price=price, notional=notional, fee=fee))
				self.__logs.append(self.__opened_position_log())

			self.store._add_trade([self.__data.datetime, ORDER_SIDE_BUY, quantity, price, notional, fee, math.nan])
			self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_COMMISSION, fee * -1])
			self.__logs.append(f"Cash after {self.broker.cash:.{self.cfg.quote_precision}f}")

	@final
	def __sell(self, quantity: float, price: float, reduce_only: bool = False, is_maker: bool = False):
		if math.isnan(price) or price == 0:
			raise Exception("Price is required.")

		if math.isnan(quantity) or quantity == 0:
			raise Exception("Quantity is required.")

		fee_rate = self.cfg.maker_fee_rate if is_maker else self.cfg.taker_fee_rate
		self.__logs.append(self.__ohlc_log())
		self.__logs.append(f"Cash before {self.broker.cash:.{self.cfg.quote_precision}f}")

		if reduce_only:
			if self.__position is not None:
				if self.__position.side != POSITION_SIDE_LONG:
					raise Exception(f"Wrong order side to reduce {self.__position.side} position.")

				rqty = quantity

				if quantity > self.__position.size:
					rqty = self.__position.size

				pnl = (price - self.__position.avg_price) * rqty
				notional = price * rqty
				fee = notional * fee_rate
				margin = (self.__position.avg_price * rqty) * (1 / self.__position.leverage)
				self.broker._add_cash(margin + pnl - fee)
				self.__position._decrease(rqty)
				self.store._add_trade([self.__data.datetime, ORDER_SIDE_SELL, rqty, price, notional, fee, pnl])
				self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_REALIZED_PNL, pnl])
				self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_COMMISSION, fee * -1])
				self.__logs.append(self.__trade_log(side=ORDER_SIDE_SELL, quantity=rqty, price=price, notional=notional, fee=fee))

				if self.__position.size > 0:
					self.__logs.append(self.__reduced_position_log(quantity=rqty, margin=margin))
					self.__logs.append(self.__current_position_log())
				else:
					self.__logs.append(self.__closed_position_log())
					self.__position = None

				self.__logs.append(f"Realized PNL {pnl:.{self.cfg.quote_precision}f}")
				self.__logs.append(f"Cash after {self.broker.cash:.{self.cfg.quote_precision}f}")
			else:
				raise Exception("No opened positions to reduce size.")
		else:
			notional = price * quantity
			fee = notional * fee_rate

			if self.__position is not None:
				margin = notional * (1 / self.__position.leverage)

				if self.broker.cash < margin + fee:
					raise Exception("Insufficient funds.")

				self.__position._increase(price, quantity)
				self.broker._sub_cash(margin + fee)
				self.__logs.append(self.__trade_log(side=ORDER_SIDE_SELL, quantity=quantity, price=price, notional=notional, fee=fee))
				self.__logs.append(self.__increased_position_log(quantity=quantity, margin=margin))
				self.__logs.append(self.__current_position_log())
			else:
				margin = notional * (1 / self.cfg.leverage)

				if self.broker.cash < margin + fee:
					raise Exception("Insufficient funds.")

				self.__position = Position(
					side=POSITION_SIDE_SHORT,
					price=price,
					size=quantity,
					created_at=self.__data.datetime,
					leverage=self.cfg.leverage
				)

				self.broker._sub_cash(margin + fee)
				self.__logs.append(self.__trade_log(side=ORDER_SIDE_SELL, quantity=quantity, price=price, notional=notional, fee=fee))
				self.__logs.append(self.__opened_position_log())

			self.store._add_trade([self.__data.datetime, ORDER_SIDE_SELL, quantity, price, notional, fee, math.nan])
			self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_COMMISSION, fee * -1])
			self.__logs.append(f"Cash after {self.broker.cash:.{self.cfg.quote_precision}f}")

	@final
	def __skip_next(self) -> bool:
		if self.__data is None:
			return True
		elif math.isnan(self.__data.open) or math.isnan(self.__data.high) or math.isnan(self.__data.low) or math.isnan(self.__data.close):
			return True

		return False

	@final
	def __before_next(self):
		self.__logs = []

		if self.__position is not None:
			if self.cfg.leverage > 1 or self.__position.side == POSITION_SIDE_SHORT:
				if self.__data.datetime.hour in self.cfg.funding_rate_hours and self.__data.datetime.minute == 0:
					fee = self.__position.notional * self.cfg.funding_rate
					self.broker._sub_cash(fee)
					self.store._add_transaction([self.__data.datetime, TRANSACTION_TYPE_FUNDING_FEE, fee * -1])
					self.__logs.append(f"Funding fee of {fee:.{self.cfg.quote_precision}f} paid successfully")

	@final
	def __after_next(self):
		amount = self.broker.cash

		if self.__position is not None:
			amount += self.__position.margin + self.__position.get_unrealized_pnl(self.__data.close)

		self.store._add_portfolio_history([self.__data.datetime, amount])

		if self.cfg.debug:
			self.__print_logs()

	@property
	def data(self) -> tuple:
		return self.__data

	@property
	def position(self) -> Position:
		return self.__position

	@final
	def write_log(self, msg: str):
		self.__logs.append(msg)

	@final
	def buy(self, quantity: float, price: float = 0, reduce_only: bool = False):
		buy_price = self.__data.close
		is_maker = False

		if price > 0:
			if price > self.__data.high or price < self.__data.low:
				raise Exception(f"Wrong price {price}. Price must be <= {self.__data.high} and >= {self.__data.low}")

			buy_price = price

			if not reduce_only:
				is_maker = True

		self.__buy(quantity=quantity, price=buy_price, reduce_only=reduce_only, is_maker=is_maker)

	@final
	def sell(self, quantity: float, price: float = 0, reduce_only: bool = False):
		sell_price = self.__data.close
		is_maker = False

		if price > 0:
			if price > self.__data.high or price < self.__data.low:
				raise Exception(f"Wrong price {price}. Price must be <= {self.__data.high} and >= {self.__data.low}")

			sell_price = price

			if not reduce_only:
				is_maker = True

		self.__sell(quantity=quantity, price=sell_price, reduce_only=reduce_only, is_maker=is_maker)

	def next(self):
		pass

	@final
	def run(self) -> Report:
		if self.store.raw_data is None:
			raise Exception("Data feed is empty.")

		if self.broker.cash == 0:
			raise Exception("Insufficient funds.")

		start = dt.datetime.now(timezone.utc)

		for row in self.store.raw_data.itertuples():
			self.__data = row

			if self.__skip_next():
				continue

			self.__before_next()
			self.next()
			self.__after_next()

		end = dt.datetime.now(timezone.utc)
		duration = end - start

		return Report(
			strategy=self.__class__.__name__,
			duration=duration,
			broker=self.broker,
			cfg=self.cfg,
			store=self.store,
		)
