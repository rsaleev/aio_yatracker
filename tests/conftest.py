import os

import pytest

from aio_yatracker.base import BaseClient


@pytest.fixture(autouse=True)
async def get_client():
    async with BaseClient(
        os.environ["YANDEX_TOKEN"], os.environ["TRACKER_ORG_ID"]
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def get_primary_queue_id():
    return "TESTCLIENT"


@pytest.fixture(autouse=True)
def get_secondary_queue_id():
    return "TESTCLIENTRESER"


@pytest.fixture(autouse=True)
def get_primary_issue_id():
    return "TESTCLIENT-1"


@pytest.fixture(autouse=True)
def get_secondary_issue_id():
    return "TESTCLIENTRESER-1"
