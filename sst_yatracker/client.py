import typing

from aiohttp import ClientSession, ClientResponse, ClientRequest
from types import TracebackType
from .base import TrackerModel, ResponseParams




class TrackerClient:
    def __init__(self, token: str, org_id: str):
        self._url = "https://api.tracker.yandex.net"
        self._token = token
        self._org_id = org_id
        self._params = {'page':1, 'perPage':100}
        self._headers = {
            "Authorization": f"OAuth {self._token}",
            "X-Org-ID": self._org_id,
        }

    async def __aenter__(self) -> "TrackerClient":
        self.session = ClientSession(base_url=self._url, raise_for_status=True)
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        await self.session.close()

    async def post(
        self,
        url: str,
        data: TrackerModel,
        params: typing.Dict[str, typing.Any],
        response_model: TrackerModel | None = None,
    ) -> TrackerModel | None:
        r = await self.session.post(url=url, params=params, data=data)
       
    async def get(
        self,
        url: str,
        params: typing.Dict[str, typing.Any] = {},
        response_model: TrackerModel | None = None,
    ) -> TrackerModel | None:
        r = await self.session.get(url=url, params=params)
        
    async def patch(
        self,
        url: str,
        params: typing.Dict[str, typing.Any] = {},
        response_model: TrackerModel | None = None,
    ) -> TrackerModel | None:
        ...


    async def handle_response(self, params, request:ClientRequest,  response:ClientResponse, response_model:TrackerModel|None):
        response_pagination = ResponseParams(**response.headers)
        data = await response.json()
        if len(data) < response_pagination.total_count:
            
       