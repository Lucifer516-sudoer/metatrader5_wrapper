class MT5Error(Exception):
    """
    Core MT5 Error
    """


class MT5ConnectionError(MT5Error):
    """Raised when not able to connect to the MT5 terminal"""
