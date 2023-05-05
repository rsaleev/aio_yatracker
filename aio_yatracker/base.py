import asyncio
import typing
from datetime import datetime
from types import TracebackType

from aiohttp import ClientResponse, ClientSession
from pydantic import BaseModel, Field


def to_camel_case(arg: str) -> str:
    string_split = arg.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


def to_snake_case(arg: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in arg]).lstrip("_")


def convert_datetime_to_iso_8601(arg: datetime) -> str:
    return arg.astimezone().isoformat(sep="T", timespec="milliseconds")


def convert_iso_8601_to_datetime(arg: str):
    return datetime.fromisoformat(arg)


class TrackerModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        use_enum_values = True
        allow_mutation = True
        json_encoders = {
            datetime: convert_datetime_to_iso_8601,
        }


class RequestParams(BaseModel):
    per_page: int = 100
    page: int = 1

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case


class ResponseParams(BaseModel):
    total_pages: int | None = Field(default=None, alias="X-Total-Pages")
    total_count: int | None = Field(default=None, alias="X-Total-Count")

    class Config:
        allow_population_by_field_name = True


class BaseClient:
    def __init__(self, token: str, org_id: str):
        self._url = "https://api.tracker.yandex.net"
        self._version = "v2"
        self._token = token
        self._org_id = org_id
        self._params = {"page": 1, "perPage": 100}
        self._headers = {
            "Authorization": f"OAuth {self._token}",
            "X-Org-ID": self._org_id,
        }

    async def __aenter__(self) -> "BaseClient":
        self.session = ClientSession(
            base_url=f"{self._url}", raise_for_status=True, headers=self._headers
        )
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        await self.session.close()

    async def get(
        self,
        url: str,
        params: typing.Dict[str, typing.Any] | None = None,
    ) -> dict | typing.List[dict] | None:
        """
        get реализация GET запроса

        :param url: путь endpoint'a
        :type url: str
        :param params: параметры запроса, defaults to None
        :type params: typing.Dict[str, typing.Any] | None, optional
        :return: _description_
        :rtype: dict |typing.List[dict]| None
        """
        response = await self.session.request(
            "GET", f"/{self._version}/{url}", params=params
        )
        return await self._handle_response("GET", url, None, params, response)

        # if response.text:
        #     return await response.json()
        # return

    async def post(
        self,
        url: str,
        data: TrackerModel,
        params: typing.Dict[str, typing.Any] | None = None,
    ) -> dict | None:
        response = await self.session.request(
            "POST",
            f"/{self._version}/{url}",
            params=params,
            data=data.json(by_alias=True),
        )
        return await self._handle_response(
            "POST",
            f"/{self._version}/{url}",
            data=data,
            params=params,
            response=response,
        )

    async def _handle_response(
        self,
        method: str,
        url: str,
        data: TrackerModel | None,
        params: typing.Dict[str, typing.Any] | None,
        response: ClientResponse,
    ):
        request_pagination = RequestParams()
        if params:
            request_pagination = RequestParams.parse_obj(params)
        response_pagination = ResponseParams.parse_obj(response.headers)
        if (
            response_pagination.total_count
            and response_pagination.total_count != request_pagination.per_page
            and response_pagination.total_pages
            and response_pagination.total_pages > 1
        ):
            expanded, _ = await asyncio.gather(
                *[
                    self._retrieve_paginated_data(
                        method, url, data, params, page, request_pagination.per_page
                    )
                    for page in range(1, response_pagination.total_pages + 1)
                ]
            )
            return expanded
        else:
            if response.text:
                return await response.json()
            else:
                return

    async def _retrieve_paginated_data(
        self,
        method,
        url: str,
        data: TrackerModel | None,
        params: typing.Dict[str, typing.Any] | None,
        paginated_page: int,
        paginated_items_per_page: int,
    ):
        paginated_params = RequestParams(
            per_page=paginated_items_per_page, page=paginated_page
        )
        if params:
            params.update(paginated_params.dict(by_alias=True))
        else:
            params = paginated_params.dict(by_alias=True)
        response = await self.session.request(
            method, f"/{self._version}/{url}", params=params
        )
        return await response.json()
