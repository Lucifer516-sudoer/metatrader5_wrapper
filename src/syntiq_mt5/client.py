from __future__ import annotations

import logging
from datetime import datetime
from time import perf_counter

from syntiq_mt5._core.errors import MT5ErrorInfo
from syntiq_mt5._core.execution import Result
from syntiq_mt5.account.models import AccountInfo
from syntiq_mt5.account.service import AccountService
from syntiq_mt5.connection.models import LoginCredential
from syntiq_mt5.connection.service import ConnectionService
from syntiq_mt5.history.models import Deal
from syntiq_mt5.history.service import HistoryService
from syntiq_mt5.market.candles import Candle
from syntiq_mt5.market.symbols import MarketService
from syntiq_mt5.market_book.models import BookEntry
from syntiq_mt5.market_book.service import MarketBookService
from syntiq_mt5.orders.models import HistoricalOrder, Order, TradeRequest, TradeResult
from syntiq_mt5.orders.service import OrderService
from syntiq_mt5.positions.models import Position
from syntiq_mt5.positions.service import PositionService
from syntiq_mt5.symbols.models import SymbolInfo, SymbolTick
from syntiq_mt5.symbols.service import SymbolService
from syntiq_mt5.terminal.models import TerminalInfo
from syntiq_mt5.terminal.service import TerminalService
from syntiq_mt5.ticks.models import Tick
from syntiq_mt5.ticks.service import TickService


class MetaTrader5Client:
    def __init__(self, *, debug: bool = False) -> None:
        self.connection = ConnectionService()
        self._positions = PositionService()
        self.market = MarketService()
        self._account = AccountService()
        self._terminal = TerminalService()
        self._symbols = SymbolService()
        self._market_book = MarketBookService()
        self._ticks = TickService()
        self._orders = OrderService()
        self._history = HistoryService()
        self._initialized = False
        self._logged_in = False
        self._debug = debug
        self._logger = logging.getLogger("syntiq_mt5")

    def __enter__(self) -> MetaTrader5Client:
        return self

    def __exit__(self, *_: object) -> None:
        shutdown_result = self.shutdown()
        if self._debug and not shutdown_result.success:
            self._logger.error("[MT5] shutdown | failure | code=%s", shutdown_result.error_code)

    def _log_result(self, name: str, result: Result[object] | Result[None], started: float) -> None:
        if not self._debug:
            return
        elapsed_ms = int((perf_counter() - started) * 1000)
        status = "success" if result.success else "failure"
        code = 0 if result.success else result.error_code
        self._logger.debug("[MT5] %s | %s | code=%s | %sms", name, status, code, elapsed_ms)

    def _guard_initialized(self, operation: str) -> Result[None] | None:
        if self._initialized:
            return None
        return Result.fail(
            MT5ErrorInfo(code=-10, message="Client not initialized. Call initialize() first."),
            context=operation,
            operation=operation,
        )

    def _guard_result(self, operation: str) -> Result[object] | None:
        guard = self._guard_initialized(operation)
        if guard is None:
            return None
        return Result.fail(
            MT5ErrorInfo(
                code=guard.error_code or -10,
                message=guard.error_message or "Client not initialized. Call initialize() first.",
            ),
            context=operation,
            operation=operation,
        )

    def initialize(self, credentials: LoginCredential | None = None) -> Result[None]:
        started = perf_counter()
        result = self.connection.initialize(credentials)
        self._initialized = result.success
        self._log_result("initialize", result, started)
        return result

    def login(self, credentials: LoginCredential) -> Result[None]:
        guard = self._guard_initialized("login")
        if guard is not None:
            self._log_result("login", guard, perf_counter())
            return guard
        started = perf_counter()
        result = self.connection.login(credentials)
        self._logged_in = result.success
        self._log_result("login", result, started)
        return result

    def shutdown(self) -> Result[None]:
        started = perf_counter()
        result = self.connection.shutdown()
        self._initialized = False
        self._logged_in = False
        self._log_result("shutdown", result, started)
        return result

    def version(self) -> Result[tuple[int, int, str]]:
        guard = self._guard_result("version")
        if guard is not None:
            return Result[tuple[int, int, str]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.connection.version()
        self._log_result("version", Result[object].model_validate(result.model_dump()), started)
        return result

    def positions(self, symbol: str | None = None) -> Result[list[Position]]:
        guard = self._guard_result("positions_get")
        if guard is not None:
            return Result[list[Position]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._positions.positions(symbol=symbol)
        self._log_result("positions_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def positions_total(self) -> Result[int]:
        guard = self._guard_result("positions_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._positions.positions_total()
        self._log_result("positions_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        guard = self._guard_result("copy_rates_from_pos")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.get_candles(symbol=symbol, timeframe=timeframe, count=count)
        self._log_result(
            "copy_rates_from_pos", Result[object].model_validate(result.model_dump()), started
        )
        return result

    # Account Information
    def account_info(self) -> Result[AccountInfo]:
        guard = self._guard_result("account_info")
        if guard is not None:
            return Result[AccountInfo].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._account.account_info()
        self._log_result("account_info", Result[object].model_validate(result.model_dump()), started)
        return result

    # Terminal Information
    def terminal_info(self) -> Result[TerminalInfo]:
        guard = self._guard_result("terminal_info")
        if guard is not None:
            return Result[TerminalInfo].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._terminal.terminal_info()
        self._log_result("terminal_info", Result[object].model_validate(result.model_dump()), started)
        return result

    # Symbol Operations
    def symbols_total(self) -> Result[int]:
        guard = self._guard_result("symbols_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbols_total()
        self._log_result("symbols_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbols_get(self, group: str | None = None) -> Result[list[str]]:
        guard = self._guard_result("symbols_get")
        if guard is not None:
            return Result[list[str]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbols_get(group=group)
        self._log_result("symbols_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbol_select(self, symbol: str, enable: bool) -> Result[bool]:
        guard = self._guard_result("symbol_select")
        if guard is not None:
            return Result[bool].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbol_select(symbol=symbol, enable=enable)
        self._log_result("symbol_select", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbol_info(self, symbol: str) -> Result[SymbolInfo]:
        guard = self._guard_result("symbol_info")
        if guard is not None:
            return Result[SymbolInfo].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbol_info(symbol=symbol)
        self._log_result("symbol_info", Result[object].model_validate(result.model_dump()), started)
        return result

    def symbol_info_tick(self, symbol: str) -> Result[SymbolTick]:
        guard = self._guard_result("symbol_info_tick")
        if guard is not None:
            return Result[SymbolTick].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._symbols.symbol_info_tick(symbol=symbol)
        self._log_result("symbol_info_tick", Result[object].model_validate(result.model_dump()), started)
        return result

    # Market Book Operations
    def market_book_add(self, symbol: str) -> Result[bool]:
        guard = self._guard_result("market_book_add")
        if guard is not None:
            return Result[bool].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._market_book.market_book_add(symbol=symbol)
        self._log_result("market_book_add", Result[object].model_validate(result.model_dump()), started)
        return result

    def market_book_get(self, symbol: str) -> Result[list[BookEntry]]:
        guard = self._guard_result("market_book_get")
        if guard is not None:
            return Result[list[BookEntry]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._market_book.market_book_get(symbol=symbol)
        self._log_result("market_book_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def market_book_release(self, symbol: str) -> Result[bool]:
        guard = self._guard_result("market_book_release")
        if guard is not None:
            return Result[bool].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._market_book.market_book_release(symbol=symbol)
        self._log_result("market_book_release", Result[object].model_validate(result.model_dump()), started)
        return result

    # Historical Rates
    def copy_rates_from(
        self, symbol: str, timeframe: int, date_from: datetime, count: int
    ) -> Result[list[Candle]]:
        guard = self._guard_result("copy_rates_from")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.copy_rates_from(
            symbol=symbol, timeframe=timeframe, date_from=date_from, count=count
        )
        self._log_result("copy_rates_from", Result[object].model_validate(result.model_dump()), started)
        return result

    def copy_rates_range(
        self, symbol: str, timeframe: int, date_from: datetime, date_to: datetime
    ) -> Result[list[Candle]]:
        guard = self._guard_result("copy_rates_range")
        if guard is not None:
            return Result[list[Candle]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self.market.copy_rates_range(
            symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to
        )
        self._log_result("copy_rates_range", Result[object].model_validate(result.model_dump()), started)
        return result

    # Tick Data
    def copy_ticks_from(
        self, symbol: str, date_from: datetime, count: int, flags: int
    ) -> Result[list[Tick]]:
        guard = self._guard_result("copy_ticks_from")
        if guard is not None:
            return Result[list[Tick]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._ticks.copy_ticks_from(
            symbol=symbol, date_from=date_from, count=count, flags=flags
        )
        self._log_result("copy_ticks_from", Result[object].model_validate(result.model_dump()), started)
        return result

    def copy_ticks_range(
        self, symbol: str, date_from: datetime, date_to: datetime, flags: int
    ) -> Result[list[Tick]]:
        guard = self._guard_result("copy_ticks_range")
        if guard is not None:
            return Result[list[Tick]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._ticks.copy_ticks_range(
            symbol=symbol, date_from=date_from, date_to=date_to, flags=flags
        )
        self._log_result("copy_ticks_range", Result[object].model_validate(result.model_dump()), started)
        return result

    # Order Operations
    def orders_total(self) -> Result[int]:
        guard = self._guard_result("orders_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.orders_total()
        self._log_result("orders_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def orders_get(
        self, symbol: str | None = None, group: str | None = None, ticket: int | None = None
    ) -> Result[list[Order]]:
        guard = self._guard_result("orders_get")
        if guard is not None:
            return Result[list[Order]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.orders_get(symbol=symbol, group=group, ticket=ticket)
        self._log_result("orders_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_calc_margin(self, action: int, symbol: str, volume: float, price: float) -> Result[float]:
        guard = self._guard_result("order_calc_margin")
        if guard is not None:
            return Result[float].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_calc_margin(action=action, symbol=symbol, volume=volume, price=price)
        self._log_result("order_calc_margin", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_calc_profit(
        self, action: int, symbol: str, volume: float, price_open: float, price_close: float
    ) -> Result[float]:
        guard = self._guard_result("order_calc_profit")
        if guard is not None:
            return Result[float].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_calc_profit(
            action=action, symbol=symbol, volume=volume, price_open=price_open, price_close=price_close
        )
        self._log_result("order_calc_profit", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_check(self, request: TradeRequest) -> Result[TradeResult]:
        guard = self._guard_result("order_check")
        if guard is not None:
            return Result[TradeResult].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_check(request=request)
        self._log_result("order_check", Result[object].model_validate(result.model_dump()), started)
        return result

    def order_send(self, request: TradeRequest) -> Result[TradeResult]:
        guard = self._guard_result("order_send")
        if guard is not None:
            return Result[TradeResult].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._orders.order_send(request=request)
        self._log_result("order_send", Result[object].model_validate(result.model_dump()), started)
        return result

    # History Operations
    def history_orders_total(self, date_from: datetime, date_to: datetime) -> Result[int]:
        guard = self._guard_result("history_orders_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_orders_total(date_from=date_from, date_to=date_to)
        self._log_result("history_orders_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def history_orders_get(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Result[list[HistoricalOrder]]:
        guard = self._guard_result("history_orders_get")
        if guard is not None:
            return Result[list[HistoricalOrder]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_orders_get(
            date_from=date_from, date_to=date_to, group=group, ticket=ticket, position=position
        )
        self._log_result("history_orders_get", Result[object].model_validate(result.model_dump()), started)
        return result

    def history_deals_total(self, date_from: datetime, date_to: datetime) -> Result[int]:
        guard = self._guard_result("history_deals_total")
        if guard is not None:
            return Result[int].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_deals_total(date_from=date_from, date_to=date_to)
        self._log_result("history_deals_total", Result[object].model_validate(result.model_dump()), started)
        return result

    def history_deals_get(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Result[list[Deal]]:
        guard = self._guard_result("history_deals_get")
        if guard is not None:
            return Result[list[Deal]].model_validate(guard.model_dump())
        started = perf_counter()
        result = self._history.history_deals_get(
            date_from=date_from, date_to=date_to, group=group, ticket=ticket, position=position
        )
        self._log_result("history_deals_get", Result[object].model_validate(result.model_dump()), started)
        return result
