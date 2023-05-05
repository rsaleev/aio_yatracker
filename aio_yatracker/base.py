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


class TrackerModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        use_enum_values = True
        allow_mutating = True
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
        self._token = token
        self._org_id = org_id
        self._params = {"page": 1, "perPage": 100}
        self._headers = {
            "Authorization": f"OAuth {self._token}",
            "X-Org-ID": self._org_id,
        }

    async def __aenter__(self) -> "BaseClient":
        self.session = ClientSession(base_url=self._url, raise_for_status=True)
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
        response_model: TrackerModel | None = None,
    ) -> TrackerModel | None:
        request_params = RequestParams()
        if params:
            request_params.dict(by_alias=True).update(params)
        request = self.session.get(url=url, params=request_params)
        response = await request
        response_data = await response.json()
        return response_data

    # async def _handle_response(self, url:str, data:TrackerModel|None, params:typing.Dict[str, typing.Any] | None, response:ClientResponse, response_model: TrackerModel | None):
    #     response_pagination = ResponseParams(**response.headers)
    #     response_data = await response.json()
    #     if (
    #         response_pagination.total_count
    #         and response_pagination.total_pages
    #         and len(response_data) < response_pagination.total_count
    #         and response_pagination.total_pages > 1
    #     ):
    #         tasks = [
    #             self._retrieve_paginated_data(
    #                 url,
    #                 data,
    #                 params,
    #                 i,
    #                 request_params.per_page,
    #                 self.session.patch,
    #                 response_model,
    #             )
    #             for i in range(2, response_pagination.total_pages)
    #         ]
    #         extended = await asyncio.gather(*tasks)
    #         if response_model:
    #             return extended.append(response_model.parse_obj(response_data))
    #         return extended.append(response_data)
    #     else:
    #         if response_model:
    #             return

    # async def _retrieve_paginated_data(
    #     self,
    #     url: str,
    #     data: TrackerModel | None,
    #     params: typing.Dict[str, typing.Any] | None,
    #     paginated_page: int,
    #     paginated_items_per_page: int,
    #     request: typing.Callable,
    #     response_model: TrackerModel | None,
    # ):
    #     if params:
    #         params.update(
    #             RequestParams(
    #                 page=paginated_page, per_page=paginated_items_per_page
    #             ).dict(by_alias=True)
    #         )
    #     else:
    #         params = RequestParams(
    #             page=paginated_page, per_page=paginated_items_per_page
    #         ).dict(by_alias=True)
    #     if not data:
    #         response = await request(url, params)
    #         if response_model:
    #             return response_model.parse_obj(await response.json())
    #         return await response.json()
    #     else:
    #         response = await request(url, data, params)
    #         if response_model:
    #             return response_model.parse_obj(await response.json())
