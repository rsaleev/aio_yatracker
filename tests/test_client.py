import os

import pytest
from aiohttp import ClientSession

from aio_yatracker.base import BaseClient

@pytest.mark.asyncio
async def test_client_ceation():
    async with BaseClient(
        os.environ["YANDEX_TOKEN"], os.environ["TRACKER_ORG_ID"]
    ) as client:
        assert client.session
        assert isinstance(client.session, ClientSession)
        assert 'X-Org-ID' in client._headers.keys()
        assert 'Authorization' in client._headers.keys()


