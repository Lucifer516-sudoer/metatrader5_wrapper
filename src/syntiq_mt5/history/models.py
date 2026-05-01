from pydantic import BaseModel


class Deal(BaseModel):
    ticket: int
    order: int
    time: int
    time_msc: int
    type: int
    entry: int
    magic: int
    position_id: int
    reason: int
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    fee: float
    symbol: str
    comment: str
    external_id: str

    @property
    def net_profit(self) -> float:
        """Calculate net profit including commission, swap, and fees."""
        return self.profit + self.commission + self.swap - self.fee

    @property
    def is_entry(self) -> bool:
        """Check if deal is an entry."""
        return self.entry == 0  # DEAL_ENTRY_IN

    @property
    def is_exit(self) -> bool:
        """Check if deal is an exit."""
        return self.entry == 1  # DEAL_ENTRY_OUT

    @property
    def is_buy(self) -> bool:
        """Check if deal is a buy."""
        return self.type == 0  # DEAL_TYPE_BUY

    @property
    def is_sell(self) -> bool:
        """Check if deal is a sell."""
        return self.type == 1  # DEAL_TYPE_SELL
