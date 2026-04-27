from enum import StrEnum
from pathlib import Path

import MetaTrader5 as mt5  # type: ignore
from pydantic import BaseModel, Field, SecretStr

from metatrader5_wrapper._core.errors import MT5ConnectionError, get_last_error


class MT5ErrorResult(BaseModel):
    code: int
    message: str

    def __str__(self) -> str:
        return f"MT5Error::[{self.code}]::{self.message}"


def get_last_error() -> MT5ErrorResult:
    """Retrieves the last known error result from the MT5"""
    code, message = mt5.last_error()
    return MT5ErrorResult(code=code, message=message)


class LoginCredential(BaseModel):
    """
    Data class for credentials to login to MT5
    """

    terminal_path: Path | None = Field(default=None, description="MT5 terminal path")
    login: int = Field(description="Account Number for MT5")
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


class ConnectionStage(StrEnum):
    INITIALIZE = "initialize"
    LOGIN = "login"


class ConnectionResult(BaseModel):
    return_code: int
    message: str
    status: bool = Field(default=False)
    stage: ConnectionStage = Field(default=ConnectionStage.INITIALIZE)
    additional_message: str | None = None


def initialize(credentials: LoginCredential | None = None) -> ConnectionResult:
    """
    Initialize MT5 connection

    Args:
        credentials (LoginCredential | None, optional): The credentials to use. If not given, already logged in account will be used. Defaults to None.

    Raises:
        MT5ConnectionError: This shows that either the connection took too long to connect (or) the terminal path is wrong (or) the Login Credentials are wrong

    Returns:
        bool: `True` if the connection is established successfully otherwise, `False`
    """
    if credentials:
        try:
            error_code, message = mt5.last_error()
            if not mt5.initialize(
                path=credentials.terminal_path,
                login=credentials.login,
                password=credentials.password.get_secret_value(),
                server=credentials.server,
                timeout=credentials.timeout_in_ms,
                portable=credentials.portable,
            ):
                return ConnectionResult(
                    return_code=mt5_err[0],
                    message=mt5_err[1],
                    status=False,
                    stage=ConnectionStage.INITIALIZE,
                    additional_message=f"Unable to connect to the account: `{credentials.login}`. "
                    "Try setting higher timeout or check your MT5 login status.",
                )
            else:  # Evaluated only when the connection is successful
                error_code, message = mt5.last_error()  # type: ignore
                return ConnectionResult(
                    return_code=mt5_err[0],
                    message=mt5_err[1],
                    status=True,
                    stage=ConnectionStage.INITIALIZE,
                    additional_message=f"Got connected to the MT5 terminal with account {credentials.login} successfully.",
                )
        except Exception as err:
            raise MT5ConnectionError(
                "Couldn't connect to the Account. Please try again"
            ) from err
    else:
        try:
            result = mt5.initialize()
            error_code, message = mt5.last_error()
            if not result:
                return ConnectionResult(
                    return_code=mt5_err[0],
                    message=mt5_err[1],
                    status=False,
                    stage=ConnectionStage.INITIALIZE,
                    additional_message="Unable to connect to the account"
                    "Try setting higher timeout or check your MT5 login status.",
                )
            return ConnectionResult(
                return_code=mt5_err[0],
                message=mt5_err[1],
                status=True,
                stage=ConnectionStage.INITIALIZE,
                additional_message="Got connected to the MT5 terminal successfully.",
            )
        except Exception as err:
            raise MT5ConnectionError(
                "Couldn't connect to the Account. Please try again"
            ) from err


initialize()
