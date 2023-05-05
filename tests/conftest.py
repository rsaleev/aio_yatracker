import os

import pytest

from aio_yatracker.base import BaseClient


@pytest.fixture
async def get_client():
    async with BaseClient(
        os.environ["YANDEX_TOKEN"], os.environ["TRACKER_ORG_ID"]
    ) as client:
        yield client
