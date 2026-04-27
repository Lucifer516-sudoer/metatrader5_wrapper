from pydantic import BaseModel


class HistoryOrder(BaseModel):
    """Typed model for historical order payloads."""

    ticket: int
    time: int
    time_update: int
    type: int
    magic: int
    identifier: str
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float
    profit: float
    symbol: str
    comment: str


class HistoryDeal(BaseModel):
    """Typed model for historical deal payloads."""

    ticket: int
    time: int
    time_update: int
    type: int
    volume: float
    price: float
    profit: float
    symbol: str
    comment: str
