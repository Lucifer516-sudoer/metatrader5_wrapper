from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

from .errors import MT5ErrorInfo

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    error_code: int | None = None
    error_message: str | None = None
    context: str | None = None

    @classmethod
    def ok(cls, data: T, context: str | None = None) -> "Result[T]":
        return cls(success=True, data=data, context=context)

    @classmethod
    def fail(cls, error: MT5ErrorInfo, context: str) -> "Result[T]":
        return cls(
            success=False,
            data=None,
            error_code=error.code,
            error_message=error.message,
            context=context,
        )
