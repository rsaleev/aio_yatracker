import json
import re
from datetime import datetime

from aio_yatracker.base import ResponseParams, TrackerModel


class DefaultModel(TrackerModel):
    id: int
    val: str
    dt: datetime


def test_base_model():
    test_data = {"id": 1, "val": "Что-то надо написать", "dt": datetime.now()}
    test_output_json = DefaultModel.parse_obj(test_data).json(by_alias=True)
    test_output_dict = json.loads(test_output_json)
    assert test_output_dict["id"] == 1
    assert test_output_dict["val"] == "Что-то надо написать"
    assert re.match(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{2}:\d{2}",
        test_output_dict["dt"],
    )


def test_response_header():
    response_headers = ResponseParams.parse_obj(
        {"X-Total-Pages": 10, "X-Total-Count": 1000}
    )
    assert response_headers.total_count
    assert response_headers.total_pages
    assert response_headers.total_count == 1000
    assert response_headers.total_pages == 10
