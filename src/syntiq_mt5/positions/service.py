from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.positions.models import Position


class PositionService:
    def __init__(self) -> None:
        self._symbol_cache: dict[str, tuple[int, float]] = {}

    def positions(self, symbol: str | None = None) -> Result[list[Position]]:
        raw = call_mt5(mt5.positions_get, symbol=symbol) if symbol else call_mt5(mt5.positions_get)
        if raw.data is None:
            return Result.fail(raw.error, context="positions_get", operation="positions_get")
        rows = list(raw.data)
        symbols = {row.symbol for row in rows if row.symbol not in self._symbol_cache}
        for sym in symbols:
            info_raw = call_mt5(mt5.symbol_info, sym)
            if info_raw.data is None:
                return Result.fail(info_raw.error, context=f"symbol_info:{sym}", operation="symbol_info")
            self._symbol_cache[sym] = (int(info_raw.data.digits), float(info_raw.data.point))

        try:
            parsed = [
                Position(
                    ticket=int(row.ticket),
                    time=int(row.time),
                    time_msc=int(row.time_msc),
                    time_update=int(row.time_update),
                    time_update_msc=int(row.time_update_msc),
                    type=int(row.type),
                    magic=int(row.magic),
                    identifier=int(row.identifier),
                    reason=int(row.reason),
                    volume=float(row.volume),
                    price_open=float(row.price_open),
                    sl=float(row.sl),
                    tp=float(row.tp),
                    price_current=float(row.price_current),
                    swap=float(row.swap),
                    profit=float(row.profit),
                    symbol=str(row.symbol),
                    comment=str(row.comment),
                    external_id=str(row.external_id),
                    digits=self._symbol_cache[row.symbol][0],
                    point=self._symbol_cache[row.symbol][1],
                )
                for row in rows
            ]
        except (AttributeError, KeyError, TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1003,
                        "message": f"Invalid MT5 position payload: {exc}",
                    }
                ),
                context="positions_get",
                operation="positions_get",
            )
        return Result.ok(parsed, context="positions_get", operation="positions_get")

    def positions_total(self) -> Result[int]:
        raw = call_mt5(mt5.positions_total)
        if raw.data is None:
            return Result.fail(raw.error, context="positions_total", operation="positions_total")
        try:
            count = int(raw.data)
        except (TypeError, ValueError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1003,
                        "message": f"Invalid MT5 positions_total payload: {exc}",
                    }
                ),
                context="positions_total",
                operation="positions_total",
            )
        return Result.ok(count, context="positions_total", operation="positions_total")
