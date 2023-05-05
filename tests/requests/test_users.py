import os

import pytest

from aio_yatracker.base import BaseClient


@pytest.mark.asyncio
async def test_user_request():
    async with BaseClient(
        os.environ["YANDEX_TOKEN"], os.environ["TRACKER_ORG_ID"]
    ) as client:
        response = await client.get(url="myself")
        assert response


@pytest.mark.asyncio
async def test_users_requst():
    async with BaseClient(
        os.environ["YANDEX_TOKEN"], os.environ["TRACKER_ORG_ID"]
    ) as client:
        response = await client.get(url="users")
        assert response
        assert len(response) > 50
