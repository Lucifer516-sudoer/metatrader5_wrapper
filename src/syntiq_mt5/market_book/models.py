from pydantic import BaseModel


class BookEntry(BaseModel):
    type: int
    price: float
    volume: int
    volume_real: float

    @property
    def is_buy(self) -> bool:
        """Check if this is a buy order."""
        return self.type in (1, 3)  # BOOK_TYPE_BUY or BOOK_TYPE_BUY_MARKET

    @property
    def is_sell(self) -> bool:
        """Check if this is a sell order."""
        return self.type in (0, 2)  # BOOK_TYPE_SELL or BOOK_TYPE_SELL_MARKET
