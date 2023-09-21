from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import secrets
from static import config
from schemas import ResponseStatus, TokenResponse, ErrorResponse
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
import aiohttp


router = APIRouter()
state = secrets.token_urlsafe(16)
client = WebApplicationClient(config.client_id)


@router.get('/authorize', response_class=RedirectResponse)
async def redirect_to_auth(scope: list = []):
    return client.prepare_request_uri(
        uri=config.server_authorization_url,
        redirect_uri=config.callback_url,
        scope=scope,
        state=state,
    )


@router.get('/token', response_model=TokenResponse | ErrorResponse)
async def fetch_token(code: str, state: str):
    if state != state:
        return ErrorResponse(message='')
    token_data = client.prepare_request_body(
        code=code,
        redirect_uri=config.callback_url,
        client_id=config.client_id,
        client_secret=config.client_secret,
    )
    conn = aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=conn) as session:
            async with session.post(config.server_token_url + '?' + token_data, ssl=False) as resp:
                if resp.status != 200:
                    return ErrorResponse(message='')
                try:
                    client.parse_request_body_response(await resp.text())
                except CustomOAuth2Error:
                    return ErrorResponse(message='')
                return TokenResponse(status=ResponseStatus.OK, **client.token)
