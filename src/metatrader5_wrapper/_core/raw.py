from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from metatrader5_wrapper._core.mt5_import import mt5

from .errors import MT5ErrorInfo


@dataclass(frozen=True, slots=True)
class RawCallResult:
    data: Any
    error: MT5ErrorInfo


def call_mt5(operation: Callable[..., Any], *args: Any, **kwargs: Any) -> RawCallResult:
    data = operation(*args, **kwargs)
    code, message = mt5.last_error()
    return RawCallResult(data=data, error=MT5ErrorInfo(code=code, message=message))
