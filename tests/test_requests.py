import pytest
import os
from aiohttp import ClientSession
from aio_yatracker.base import BaseClient

@pytest.mark.asyncio
@pytest.fixture(scope='module')
async def get_client():
    async with BaseClient(os.environ['YANDEX_TOKEN'], os.environ['TRACKER_ORG_ID']) as client:
        yield client

@pytest.mark.asyncio
async def test_client():
    async with BaseClient(os.environ['YANDEX_TOKEN'], os.environ['TRACKER_ORG_ID']) as client:
        assert client
        assert client.session
  