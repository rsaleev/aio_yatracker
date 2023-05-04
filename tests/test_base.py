from datetime import datetime
import re
import json
from sst_yatracker.base import TrackerModel, ResponseParams


class TestModel(TrackerModel):
    id: int
    val: str
    dt: datetime


def test_base_model():
    test_data = {"id": 1, "val": "Что-то надо написать", "dt": datetime.now()}
    test_output_json = TestModel.parse_obj(test_data).json()
    test_output_dict = json.loads(test_output_json)
    assert test_output_dict["id"] == 1
    assert test_output_dict["val"] == "Что-то надо написать"
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}\+\d{2}:\d{2}",test_output_dict["dt"])

def test_response_header():
    params = {"X-Total-Pages":10, "X-Total-Count":1000}
    response_headers = ResponseParams(**params)
    assert response_headers.total_count == 1000
    assert response_headers.total_pages ==10
