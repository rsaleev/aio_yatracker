import re

import pytest

from aio_yatracker import macros


@pytest.mark.asyncio
async def test_list_macros(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/queues/TEST/macros/3",
            "id": 3,
            "queue": {
                "self": "https://api.tracker.yandex.net/v2/queues/TEST",
                "id": "1",
                "key": "TEST",
                "display": "Тестовая очередь",
            },
            "name": "Тестовый макрос",
            "body": "Тестовое сообщение\n{{currentUser}}{{currentDateTime.date}}{{currentDateTime}}\n{{issue.author}}",
            "fieldChanges": [
                {
                    "field": {
                        "self": "https://api.tracker.yandex.net/v2/fields/tags",
                        "id": "tags",
                        "display": "Теги",
                    },
                    "value": ["tag1", "tag2"],
                },
            ],
        },
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/queues/TEST/macros)(\?page=\d*&perPage=\d*)?"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for result in macros.list(get_client, "TEST"):
        assert all([isinstance(item, macros.MacrosResponse) for item in result])


@pytest.mark.asyncio
async def test_get_macros(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/queues/TEST/macros/3",
        "id": 3,
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/TEST",
            "id": "1",
            "key": "TEST",
            "display": "Тестовая очередь",
        },
        "name": "Тестовый макрос",
        "body": "Тестовый комментарий\n{{currentDateTime}}\n{{issue.author}}",
        "fieldChanges": [
            {
                "field": {
                    "self": "https://api.tracker.yandex.net/v2/fields/tags",
                    "id": "tags",
                    "display": "Теги",
                },
                "value": ["tag1", "tag2"],
            },
        ],
    }
    mocker.get("https://api.tracker.yandex.net/v2/queues/TEST/macros/3", payload=resp)
    r = await macros.get(get_client, "TEST", "3")
    assert isinstance(r, macros.MacrosResponse)
