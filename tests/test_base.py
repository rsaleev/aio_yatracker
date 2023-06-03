import json
import re
from datetime import datetime, timezone

from aio_yatracker.base import ResponseParams, TrackerModel


class DefaultModel(TrackerModel):
    id_value: int
    simple_string: str
    simple_datetime: datetime


def test_base_model():
    test_data = {
        "idValue": 1,
        "simpleString": "some data",
        "simpleDatetime": "2023-01-01T12:34:45.000+00:00",
    }
    test_output = DefaultModel.parse_obj(test_data)
    assert test_output.id_value == 1
    assert test_output.simple_string == "some data"
    assert test_output.simple_datetime == datetime(2023, 1, 1, 12, 34, 45,tzinfo=timezone.utc)
    test_output_json = test_output.json(by_alias=True)
    test_output_dict = json.loads(test_output_json)
    assert test_output_dict["idValue"] == 1
    assert test_output_dict["simpleString"] == "some data"
    assert re.match(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{2}:\d{2}",
        test_output_dict["simpleDatetime"],
    )


def test_response_header():
    response_headers = ResponseParams.parse_obj(
        {"X-Total-Pages": 10, "X-Total-Count": 1000}
    )
    assert response_headers.total_count
    assert response_headers.total_pages
    assert response_headers.total_count == 1000
    assert response_headers.total_pages == 10
