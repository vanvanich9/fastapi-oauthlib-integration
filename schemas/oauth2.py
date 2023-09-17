from pydantic import BaseModel
from .common import OKResponse


class AuthRequest(BaseModel):
    scope: list = []


class FetchToken(BaseModel):
    code: str
    state: str


class TokenResponse(OKResponse):
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str | None = None
    scope: list | None = None
