from pydantic import BaseModel
from .common import OKResponse


class TokenResponse(OKResponse):
    access_token: str
    token_type: str
    expires_in: int = -1
    refresh_token: str | None = None
    scope: list | None = None
