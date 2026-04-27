import MetaTrader5 as mt5  # type: ignore
from pydantic import BaseModel


class MT5Error(Exception):
    """
    Core MT5 Error
    """


class MT5ConnectionError(MT5Error):
    """Raised when not able to connect to the MT5 terminal"""


class MT5ErrorResult(BaseModel):
    code: int
    message: str

    def __str__(self) -> str:
        return f"MT5Error::[{self.code}]::{self.message}"


def get_last_error() -> MT5ErrorResult:
    """Retrieves the last known error result from the MT5"""
    code, message = mt5.last_error()
    return MT5ErrorResult(code=code, message=message)
