import typing

from aiohttp import ClientSession, ClientResponse, ClientRequest

from .base import TrackerModel




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

    async def __aexit__(self, *args, **kwargs):
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
        total_pages = response.headers.get('X-Total-Pages',1)
        total_items = response.headers.get('X-Total-Count', params[''])   
        data = await response.json()
        if len(data) < total_items:
       