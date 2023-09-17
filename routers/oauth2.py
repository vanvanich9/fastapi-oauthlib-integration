from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import secrets
from static import config
from schemas import FetchToken, ResponseStatus, TokenResponse, ErrorResponse, AuthRequest
from oauthlib.oauth2 import WebApplicationClient
import aiohttp

router = APIRouter()
state = secrets.token_urlsafe(16)
client = WebApplicationClient(config.client_id)


@router.get('/authorize', response_class=RedirectResponse)
async def redirect_to_auth(auth_data: AuthRequest = Body(...)):
    return client.prepare_request_uri(
        redirect_uri = config.callback_url,
        scope=auth_data.scope,
        state=state,
    )


@router.get('/token', response_model=TokenResponse | ErrorResponse)
async def fetch_token(data: FetchToken = Body(...)):
    if data.state != state:
        return ErrorResponse(message='')
    token_data = client.prepare_request_body(
        code=data.code,
        redirect_uri=config.callback_url,
        client_id=config.client_id,
    )
    token_url = config.server_token_url
    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, data=token_data) as resp:
            if resp.status != 200:
                return ErrorResponse(message='')
            client.parse_request_body_response(await resp.text())
            if client.token.get('status', '') == ResponseStatus.ERROR:
                return ErrorResponse(message='')
            return TokenResponse(status=ResponseStatus.OK, **client.token)


@router.get('/incomplete', response_model=ErrorResponse)
async def incomplete_fetch():
    return ErrorResponse(message='')
