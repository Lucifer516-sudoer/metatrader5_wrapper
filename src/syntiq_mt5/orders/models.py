from pydantic import BaseModel


class Order(BaseModel):
    ticket: int
    time_setup: int
    time_setup_msc: int
    time_done: int
    time_done_msc: int
    time_expiration: int
    type: int
    type_time: int
    type_filling: int
    state: int
    magic: int
    position_id: int
    position_by_id: int
    reason: int
    volume_initial: float
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    price_stoplimit: float
    symbol: str
    comment: str
    external_id: str

    @property
    def is_pending(self) -> bool:
        """Check if order is pending."""
        return self.state in (1, 3)  # ORDER_STATE_PLACED or ORDER_STATE_PARTIAL

    @property
    def is_filled(self) -> bool:
        """Check if order is filled."""
        return self.state == 4  # ORDER_STATE_FILLED

    @property
    def is_cancelled(self) -> bool:
        """Check if order is cancelled."""
        return self.state == 2  # ORDER_STATE_CANCELED


class HistoricalOrder(BaseModel):
    ticket: int
    time_setup: int
    time_setup_msc: int
    time_done: int
    time_done_msc: int
    time_expiration: int
    type: int
    type_time: int
    type_filling: int
    state: int
    magic: int
    position_id: int
    position_by_id: int
    reason: int
    volume_initial: float
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    price_stoplimit: float
    symbol: str
    comment: str
    external_id: str

    @property
    def duration_seconds(self) -> int:
        """Calculate order duration in seconds."""
        return self.time_done - self.time_setup

    @property
    def was_filled(self) -> bool:
        """Check if order was filled."""
        return self.state == 4  # ORDER_STATE_FILLED


class TradeRequest(BaseModel):
    action: int
    magic: int = 0
    order: int = 0
    symbol: str = ""
    volume: float = 0.0
    price: float = 0.0
    stoplimit: float = 0.0
    sl: float = 0.0
    tp: float = 0.0
    deviation: int = 0
    type: int = 0
    type_filling: int = 0
    type_time: int = 0
    expiration: int = 0
    comment: str = ""
    position: int = 0
    position_by: int = 0


class TradeResult(BaseModel):
    retcode: int
    deal: int
    order: int
    volume: float
    price: float
    bid: float
    ask: float
    comment: str
    request_id: int
    retcode_external: int
    request: dict[str, object] | None = None

    @property
    def is_successful(self) -> bool:
        """Check if trade was successful."""
        return self.retcode in (10008, 10009)  # TRADE_RETCODE_DONE or TRADE_RETCODE_DONE_PARTIAL

    @property
    def is_rejected(self) -> bool:
        """Check if trade was rejected."""
        return self.retcode == 10006  # TRADE_RETCODE_REJECT

    @property
    def requires_requote(self) -> bool:
        """Check if trade requires requote."""
        return self.retcode == 10004  # TRADE_RETCODE_REQUOTE
