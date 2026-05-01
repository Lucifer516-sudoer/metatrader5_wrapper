from __future__ import annotations

from syntiq_mt5._core.execution import Result
from syntiq_mt5._core.mt5_import import mt5
from syntiq_mt5._core.raw import call_mt5
from syntiq_mt5.connection.models import LoginCredential


class ConnectionService:
    def __init__(self) -> None:
        self._initialized = False

    def initialize(self, credentials: LoginCredential | None = None) -> Result[None]:
        if self._initialized:
            return Result.ok(None, context="initialize", operation="initialize")
        kwargs = {"path": credentials.path} if credentials and credentials.path else {}
        raw = call_mt5(mt5.initialize, **kwargs)
        if not raw.data:
            return Result.fail(raw.error, context="initialize", operation="initialize")
        self._initialized = True
        return Result.ok(None, context="initialize", operation="initialize")

    def login(self, credentials: LoginCredential) -> Result[None]:
        raw = call_mt5(
            mt5.login,
            login=credentials.login,
            password=credentials.password.get_secret_value(),
            server=credentials.server,
        )
        if not raw.data:
            return Result.fail(raw.error, context="login", operation="login")
        return Result.ok(None, context="login", operation="login")

    def shutdown(self) -> Result[None]:
        raw = call_mt5(mt5.shutdown)
        self._initialized = False
        if raw.data is False:
            return Result.fail(raw.error, context="shutdown", operation="shutdown")
        return Result.ok(None, context="shutdown", operation="shutdown")

    def version(self) -> Result[tuple[int, int, str]]:
        raw = call_mt5(mt5.version)
        if raw.data is None:
            return Result.fail(raw.error, context="version", operation="version")
        try:
            # MT5 version() returns tuple: (build, date, version_string)
            version_tuple = tuple(raw.data)
            if len(version_tuple) != 3:
                return Result.fail(
                    raw.error.model_copy(
                        update={
                            "code": raw.error.code if raw.error.code != 0 else -1003,
                            "message": f"Invalid MT5 version payload: expected 3 elements, got {len(version_tuple)}",
                        }
                    ),
                    context="version",
                    operation="version",
                )
            result = (int(version_tuple[0]), int(version_tuple[1]), str(version_tuple[2]))
        except (TypeError, ValueError, IndexError) as exc:
            return Result.fail(
                raw.error.model_copy(
                    update={
                        "code": raw.error.code if raw.error.code != 0 else -1003,
                        "message": f"Invalid MT5 version payload: {exc}",
                    }
                ),
                context="version",
                operation="version",
            )
        return Result.ok(result, context="version", operation="version")
