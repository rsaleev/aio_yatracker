import typing
from datetime import datetime
from types import TracebackType

from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel, Field, validator

from .utils import convert_datetime_to_iso_8601, to_camel_case

DEFAULT_PAGE = 1
DEFAULT_TOTAL_PAGES = 1
DEFAULT_TOTAL_COUNT = 50


class TrackerModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        use_enum_values = True
        json_encoders = {
            datetime: convert_datetime_to_iso_8601,
        }
        arbitrary_types_allowed = True


class RequestParams(BaseModel):
    per_page: int = DEFAULT_TOTAL_COUNT
    page: int = DEFAULT_PAGE

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case


class ResponseParams(BaseModel):
    total_pages: int = Field(default=DEFAULT_TOTAL_PAGES, alias="X-Total-Pages")
    total_count: int = Field(default=DEFAULT_TOTAL_COUNT, alias="X-Total-Count")

    class Config:
        allow_population_by_field_name = True

    @validator("total_pages")
    def validate_total_pages(cls, arg):
        if not arg:
            return DEFAULT_TOTAL_PAGES
        return arg

    @validator("total_count")
    def validate_total_count(cls, arg):
        if not arg:
            return DEFAULT_TOTAL_COUNT
        return arg


class BaseClient:
    def __init__(self, token: str, org_id: str):
        self._url = "https://api.tracker.yandex.net"
        self._version = "v2"
        self._params = RequestParams()
        self._headers = {
            "Authorization": f"OAuth {token}",
            "X-Org-ID": org_id,
        }
        self._session = ClientSession(
            base_url=f"{self._url}", raise_for_status=True, headers=self._headers
        )

    async def __aenter__(self) -> "BaseClient":
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        await self._session.close()

    async def close(self):
        await self._session.close()

    async def get(
        self,
        url: str,
        params: typing.Dict[str, typing.Any] | None = None,
    ):
        default_params = self._params.dict(by_alias=True)
        if params:
            default_params.update(params)
        return await self._session.get(f"/{self._version}/{url}", params=default_params)

    async def post(
        self,
        url: str,
        data: TrackerModel | None,
        params: typing.Dict[str, typing.Any] | None = None,
    ) -> ClientResponse:
        default_params = self._params.dict(by_alias=True)
        if params:
            default_params.update(params)
        if data:
            return await self._session.post(
                f"/{self._version}/{url}",
                params=params,
                data=data.json(by_alias=True, exclude_unset=True, exclude_none=True),
            )
        return await self._session.post(
            f"/{self._version}/{url}", params=default_params
        )

    async def patch(
        self,
        url: str,
        data: TrackerModel,
        params: typing.Dict[str, typing.Any] | None = None,
    ) -> ClientResponse:
        default_params = self._params.dict(by_alias=True)
        if params:
            default_params.update(params)
        return await self._session.patch(
            f"/{self._version}/{url}",
            params=default_params,
            data=data.json(by_alias=True, exclude_none=True),
        )

    async def delete(
        self,
        url: str,
        params: typing.Dict[str, typing.Any] | None = None,
    ) -> ClientResponse:
        return await self._session.delete(
            f"/{self._version}/{url}",params=params
        )

    async def handle_response(
        self,
        response: ClientResponse,
    ) -> ResponseParams:
        return ResponseParams.parse_obj(response.headers)
