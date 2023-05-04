import typing
from datetime import datetime

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
    perPage: int = 100
    page: int = 1


class ResponseParams(BaseModel):
    total_pages: typing.Optional[int] = Field(..., alias="X-Total-Pages")
    total_count: typing.Optional[int] = Field(..., alias="X-Total-Count")
