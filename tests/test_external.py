import re

import pytest

from aio_yatracker import external
from aio_yatracker.common import Relationship


@pytest.mark.asyncio
async def test_list_applications(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/applications/my-application",
            "id": "my-application",
            "type": "my-application",
            "name": "Application name",
        },
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/applications)(\?page=\d*&perPage=\d*)?"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for applications_list in external.applications(get_client):
        assert all(
            [
                isinstance(item, external.ApplicationLinkResponse)
                for item in applications_list
            ]
        )


@pytest.mark.asyncio
async def test_list_issues(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/issues/<issue-id>/remotelinks/51299313",
            "id": 51299313,
            "type": {
                "self": "https://api.tracker.yandex.net/v2/linktypes/relates",
                "id": "relates",
                "inward": "Linked",
                "outward": "Linked",
            },
            "direction": "outward",
            "object": {
                "self": "https://api.tracker.yandex.net/v2/applications/ru.yandex.bitbucket/objects/<object-id>",
                "id": "<object-id>",
                "key": "<object-key>",
                "application": {
                    "self": "https://api.tracker.yandex.net/v2/applications/<application-id>",
                    "id": "<application-id>",
                    "type": "<application-type>",
                    "name": "<application-name>",
                },
            },
            "createdBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000044110",
                "id": "user-name",
                "display": "display-user-name",
            },
            "updatedBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000044110",
                "id": "user-name",
                "display": "display-user-name",
            },
            "createdAt": "2021-07-14T18:59:54.552+0000",
            "updatedAt": "2021-07-14T18:59:54.552+0000",
        },
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/issues/TEST-1/remotelinks)(\?page=\d*&perPage=\d*)?"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for issues_list in external.issues(get_client, "TEST-1"):
        assert all(
            [isinstance(item, external.IssueLinkResponse) for item in issues_list]
        )


@pytest.mark.asyncio
async def test_add_external_link(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/<issue-id>/remotelinks/51455195",
        "id": 51455195,
        "type": {
            "self": "https://api.tracker.yandex.net/v2/linktypes/relates",
            "id": "relates",
            "inward": "Linked",
            "outward": "Linked",
        },
        "direction": "outward",
        "object": {
            "self": "https://api.tracker.yandex.net/v2/applications/ru.yandex.bitbucket/objects/<object-id>",
            "id": "<object-id>",
            "key": "<object-key>",
            "application": {
                "self": "https://api.tracker.yandex.net/v2/applications/<application-id>",
                "id": "<application-id>",
                "type": "<application-type>",
                "name": "<application-name>",
            },
        },
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000232694",
            "id": "user-name",
            "display": "display-user-name",
        },
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000232694",
            "id": "user-name",
            "display": "display-user-name",
        },
        "createdAt": "2021-07-19T06:18:09.327+0000",
        "updatedAt": "2021-07-19T06:18:09.327+0000",
    }
    mocker.post(
        "https://api.tracker.yandex.net/v2/issues/TEST-1/remotelinks?backlink=true",
        payload=resp,
    )
    r = await external.add(
        get_client,
        "TEST-1",
        external.IssueLinkRequest(
            relationship=Relationship.RELATES,
            key="<object key>",
            origin="<application ID>",
        ),
    )
    assert isinstance(r, external.IssueLinkResponse)


@pytest.mark.asyncio
async def test_remove_external_link(mocker, get_client):
    mocker.delete("https://api.tracker.yandex.net/v2/issues/TEST-1/remotelinks/12345")
    await external.remove(get_client, "TEST-1", 12345)
