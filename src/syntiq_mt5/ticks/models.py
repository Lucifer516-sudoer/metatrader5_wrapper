from pydantic import BaseModel


class Tick(BaseModel):
    time: int
    bid: float
    ask: float
    last: float
    volume: int
    time_msc: int
    flags: int
    volume_real: float

    @property
    def spread(self) -> float:
        """Calculate spread as ask - bid."""
        return self.ask - self.bid

    @property
    def mid_price(self) -> float:
        """Calculate mid price."""
        return (self.bid + self.ask) / 2

    @property
    def has_bid(self) -> bool:
        """Check if tick has bid price update."""
        return bool(self.flags & 2)  # TICK_FLAG_BID

    @property
    def has_ask(self) -> bool:
        """Check if tick has ask price update."""
        return bool(self.flags & 4)  # TICK_FLAG_ASK

    @property
    def has_last(self) -> bool:
        """Check if tick has last price update."""
        return bool(self.flags & 8)  # TICK_FLAG_LAST
