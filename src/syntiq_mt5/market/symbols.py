from __future__ import annotations

from datetime import datetime

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.market.candles import Candle


class MarketService:
    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        raw = call_mt5(mt5.copy_rates_from_pos, symbol, timeframe, 0, count)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_rates_from_pos", operation="copy_rates_from_pos")
        try:
            candles = [
                Candle(
                    time=int(row.time if hasattr(row, "time") else row["time"]),
                    open=float(row.open if hasattr(row, "open") else row["open"]),
                    high=float(row.high if hasattr(row, "high") else row["high"]),
                    low=float(row.low if hasattr(row, "low") else row["low"]),
                    close=float(row.close if hasattr(row, "close") else row["close"]),
                    tick_volume=int(row.tick_volume if hasattr(row, "tick_volume") else row["tick_volume"]),
                    spread=int(row.spread if hasattr(row, "spread") else row["spread"]),
                    real_volume=int(row.real_volume if hasattr(row, "real_volume") else row["real_volume"]),
                )
                for row in raw.data
            ]
        except (KeyError, AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1004,
                        "message": f"Invalid MT5 candle payload: {exc}",
                    }
                ),
                context="copy_rates_from_pos",
                operation="copy_rates_from_pos",
            )
        return Result.ok(candles, context="copy_rates_from_pos", operation="copy_rates_from_pos")

    def copy_rates_from(
        self, symbol: str, timeframe: int, date_from: datetime, count: int
    ) -> Result[list[Candle]]:
        raw = call_mt5(mt5.copy_rates_from, symbol, timeframe, date_from, count)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_rates_from", operation="copy_rates_from")
        try:
            candles = [
                Candle(
                    time=int(row.time if hasattr(row, "time") else row["time"]),
                    open=float(row.open if hasattr(row, "open") else row["open"]),
                    high=float(row.high if hasattr(row, "high") else row["high"]),
                    low=float(row.low if hasattr(row, "low") else row["low"]),
                    close=float(row.close if hasattr(row, "close") else row["close"]),
                    tick_volume=int(row.tick_volume if hasattr(row, "tick_volume") else row["tick_volume"]),
                    spread=int(row.spread if hasattr(row, "spread") else row["spread"]),
                    real_volume=int(row.real_volume if hasattr(row, "real_volume") else row["real_volume"]),
                )
                for row in raw.data
            ]
        except (KeyError, AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1004,
                        "message": f"Invalid MT5 copy_rates_from payload: {exc}",
                    }
                ),
                context="copy_rates_from",
                operation="copy_rates_from",
            )
        return Result.ok(candles, context="copy_rates_from", operation="copy_rates_from")

    def copy_rates_range(
        self, symbol: str, timeframe: int, date_from: datetime, date_to: datetime
    ) -> Result[list[Candle]]:
        raw = call_mt5(mt5.copy_rates_range, symbol, timeframe, date_from, date_to)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_rates_range", operation="copy_rates_range")
        try:
            candles = [
                Candle(
                    time=int(row.time if hasattr(row, "time") else row["time"]),
                    open=float(row.open if hasattr(row, "open") else row["open"]),
                    high=float(row.high if hasattr(row, "high") else row["high"]),
                    low=float(row.low if hasattr(row, "low") else row["low"]),
                    close=float(row.close if hasattr(row, "close") else row["close"]),
                    tick_volume=int(row.tick_volume if hasattr(row, "tick_volume") else row["tick_volume"]),
                    spread=int(row.spread if hasattr(row, "spread") else row["spread"]),
                    real_volume=int(row.real_volume if hasattr(row, "real_volume") else row["real_volume"]),
                )
                for row in raw.data
            ]
        except (KeyError, AttributeError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1004,
                        "message": f"Invalid MT5 copy_rates_range payload: {exc}",
                    }
                ),
                context="copy_rates_range",
                operation="copy_rates_range",
            )
        return Result.ok(candles, context="copy_rates_range", operation="copy_rates_range")
