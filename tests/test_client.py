import os

import pytest
from aiohttp import ClientSession

from aio_yatracker.base import BaseClient


@pytest.mark.asyncio
async def test_client_ceation():
    async with BaseClient("token", "organization_id") as client:
        assert client._session
        assert isinstance(client._session, ClientSession)
        assert "X-Org-ID" in client._headers.keys()
        assert "Authorization" in client._headers.keys()
