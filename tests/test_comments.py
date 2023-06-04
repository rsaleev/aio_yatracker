import re

import pytest

from aio_yatracker import comments


@pytest.mark.asyncio
async def test_add_comment(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/TREK-1/comments/626",
        "id": 626,
        "longId": "5fa15a24ac894475dd14ff07",
        "text": "<comment text>",
        "createBody": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<user ID>",
            "display": "<user's name displayed",
        },
        "updateBody": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<user ID>",
            "display": "<user's name displayed",
        },
        "createdAt": "2020-11-03T13:24:52.575+0000",
        "updatedAt": "2020-11-03T13:24:52.575+0000",
        "summonees": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016576",
                "id": "<user ID>",
                "display": "<user's name displayed",
            }
        ],
        "maillistSummonees": [
            {
                "self": "https://api.tracker.yandex.net/v2/maillists/usertest@test.ru",
                "id": "<mailing list address>",
                "display": "<mailing list name displayed>",
            }
        ],
        "version": 1,
        "type": "standard",
        "transport": "internal",
    }

    mocker.post(
        "https://api.tracker.yandex.net/v2/issues/TREK-1/comments", payload=resp
    )
    r = await comments.add(
        get_client, "TREK-1", data=comments.CommentCreateRequest(text="<comment text>")
    )
    assert isinstance(r, comments.CommentCreateResponse)
    assert r.text == "<comment text>"


@pytest.mark.asyncio
async def test_list_comments(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2/comments/9849018",
            "id": 9849018,
            "longId": "5fa15a24ac894475dd14ff07",
            "text": "Comment",
            "createdBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "updatedBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "createdAt": "2017-06-11T05:11:12.347+0000",
            "updatedAt": "2017-06-11T05:11:12.347+0000",
            "version": 1,
            "type": "standard",
            "transport": "internal",
        },
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/issues/JUNE-2/comments)(\?page=\d*&perPage=\d*)?"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for comments_list in comments.list(get_client, "JUNE-2"):
        assert isinstance(comments_list, list)
        assert all(
            [isinstance(item, comments.CommentListResponse) for item in comments_list]
        )


@pytest.mark.asyncio
async def test_edit_comment(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/TREK-1/comments/684",
        "id": "684",
        "longId": "5fc4bc634e121b12f44a0488",
        "text": "<comment text>",
        "createBody": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<user ID>",
            "display": "<user's name displayed",
        },
        "updateBody": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<user ID>",
            "display": "<user's name displayed",
        },
        "createdAt": "2020-11-30T09:33:23.638+0000",
        "updatedAt": "2020-11-30T09:39:07.631+0000",
        "summonees": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016576",
                "id": "<user ID>",
                "display": "<user's name displayed",
            }
        ],
        "maillistSummonees": [
            {
                "self": "https://api.tracker.yandex.net/v2/maillists/usertest@test.ru",
                "id": "<mailing list address>",
                "display": "<mailing list name displayed>",
            }
        ],
        "version": 2,
        "type": "standard",
        "transport": "internal",
    }
    mocker.patch("https://api.tracker.yandex.net/v2/issues/TREK-1/comments/684", payload=resp)
    r = await comments.edit(
        get_client, "TREK-1", 684, comments.CommentEditRequest(text="<comment text>")
    )
    assert isinstance(r, comments.CommentEditResponse)
