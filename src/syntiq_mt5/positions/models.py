from pydantic import BaseModel


class Position(BaseModel):
    ticket: int
    time: int = 0
    time_msc: int = 0
    time_update: int = 0
    time_update_msc: int = 0
    type: int
    magic: int = 0
    identifier: int = 0
    reason: int = 0
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float = 0.0
    profit: float = 0.0
    symbol: str
    comment: str = ""
    external_id: str = ""
    digits: int
    point: float

    @property
    def pip_size(self) -> float:
        return self.point * 10 if self.digits in (3, 5) else self.point

    @property
    def pips_profit(self) -> float:
        direction = 1 if self.type == 0 else -1
        return ((self.price_current - self.price_open) * direction) / self.pip_size

    @property
    def pips_to_tp(self) -> float:
        if self.tp == 0:
            return 0.0
        direction = 1 if self.type == 0 else -1
        return ((self.tp - self.price_current) * direction) / self.pip_size
