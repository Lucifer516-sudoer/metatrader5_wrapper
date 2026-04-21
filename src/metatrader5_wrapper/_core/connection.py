from pathlib import Path

import MetaTrader5 as mt5  # type: ignore
from pydantic import BaseModel, Field, SecretStr

from metatrader5_wrapper.errors import MT5ConnectionError


class LoginCredential(BaseModel):
    """
    Data class for credentials to login to MT5
    """

    terminal_path: Path | None = Field(default=None, description="MT5 terminal path")
    login: str = Field(description="Account Number for MT5")
    password: SecretStr = Field(description="Account password")
    server: str = Field(description="Server's name")
    timeout: int = Field(default=15, description="Connection timeout in seconds")
    portable: bool = Field(
        default=False, description="Flag the terminal to launch with portable mode"
    )

    @property
    def timeout_in_ms(self) -> int:
        """Converts the seconds to milliseconds"""
        return self.timeout * 1_000  # 10^3


def initialize(credentials: LoginCredential | None = None) -> bool:
    """
    Initialize MT5 connection

    Args:
        credentials (LoginCredential | None, optional): The credentials to use. If not given, already logged in account will be used. Defaults to None.

    Raises:
        MT5ConnectionError: This shows that either the connection took too long to connect (or) the terminal path is wrong (or) the Login Credentials are wrong

    Returns:
        bool: `True` if the connection is established successfully otherwise, `False`
    """
    result: bool

    if credentials is not None:
        result = mt5.initialize(
            credentials.terminal_path,
            login=credentials.login,
            password=credentials.password.get_secret_value(),
            server=credentials.server,
            timeout=credentials.timeout_in_ms,
            portable=credentials.portable,
        )

        if not result:
            raise MT5ConnectionError(
                f"Unable to connect to the account: `{credentials.login}`. "
                "Try setting higher timeout or check your MT5 login status."
            )

    else:
        result = mt5.initialize()

        if not result:
            raise MT5ConnectionError(
                "Unable to connect with the default logged in account. "
                "Provide credentials or try again."
            )

    return result
