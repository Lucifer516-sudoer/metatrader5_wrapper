from pydantic import BaseModel, SecretStr


class LoginCredentials(BaseModel):
    login: int
    password: SecretStr
    server: str
    path: str | None = None
