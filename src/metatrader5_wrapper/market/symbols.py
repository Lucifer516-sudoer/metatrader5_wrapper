from __future__ import annotations

from metatrader5_wrapper._core.mt5_import import mt5

from metatrader5_wrapper._core.execution import Result
from metatrader5_wrapper._core.raw import call_mt5
from metatrader5_wrapper.market.candles import Candle


class MarketService:
    def get_candles(self, symbol: str, timeframe: int, count: int) -> Result[list[Candle]]:
        raw = call_mt5(mt5.copy_rates_from_pos, symbol, timeframe, 0, count)
        if raw.data is None:
            return Result.fail(raw.error, context="copy_rates_from_pos")
        candles = [
            Candle(
                time=int(row["time"]),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
            )
            for row in raw.data
        ]
        return Result.ok(candles, context="copy_rates_from_pos")
