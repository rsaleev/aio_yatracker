import os

import pytest
import pytest_asyncio
from aioresponses import aioresponses

from aio_yatracker.base import BaseClient


@pytest_asyncio.fixture()
async def get_client():
    async with BaseClient(os.environ['YANDEX_TOKEN'], os.environ['TRACKER_ORG_ID']) as client:
        yield client

@pytest.fixture
def mocker():
    with aioresponses() as m:
        yield m
