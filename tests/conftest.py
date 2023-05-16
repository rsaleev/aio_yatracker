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
def get_queue_id():
    return "SSTGARBAGE"


@pytest.fixture(autouse=True)
def get_issue_id():
    return "SSTGARBAGE-1436"
