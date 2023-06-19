import re

import pytest

from aio_yatracker import attachments
from tempfile import TemporaryFile


@pytest.mark.asyncio
async def test_list_attachments(mocker, get_client):
    resp = [
        {
            "self": "<address of the API resource corresponding to the file attached>",
            "id": "<file ID>",
            "name": "<file name>",
            "content": "<address to download the file from>",
            "thumbnail": "<address to download the preview from>",
            "createdBy": {
                "self": "<resource corresponding to the file author>",
                "id": "<username of the file author>",
                "display": "<name of the file author>",
            },
            "createdAt": "2021-01-01T17:34:34",
            "mimetype": "<file data type>",
            "size": 11,
            "metadata": {"size": 1024},
        },
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/issues/JUNE-2/attachments)(\?page=\d*&perPage=\d*)?$"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for attachment_list in attachments.list(get_client, "JUNE-2"):
        assert all(
            [isinstance(item, attachments.Attachment) for item in attachment_list]
        )
    

