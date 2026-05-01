from pydantic import BaseModel


class TerminalInfo(BaseModel):
    community_account: bool
    community_connection: bool
    connected: bool
    dlls_allowed: bool
    trade_allowed: bool
    tradeapi_disabled: bool
    email_enabled: bool
    ftp_enabled: bool
    notifications_enabled: bool
    mqid: bool
    build: int
    maxbars: int
    codepage: int
    ping_last: int
    community_balance: float
    retransmission: float
    company: str
    name: str
    language: str
    path: str
    data_path: str
    commondata_path: str

    @property
    def version(self) -> str:
        """Return terminal version as string."""
        return f"Build {self.build}"

    @property
    def is_ready_for_trading(self) -> bool:
        """Check if terminal is ready for trading."""
        return self.connected and self.trade_allowed and not self.tradeapi_disabled
