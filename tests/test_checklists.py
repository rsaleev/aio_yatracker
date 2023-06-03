from datetime import datetime

import pytest

from aio_yatracker import checklists


@pytest.mark.asyncio
async def test_create_checklist(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/ORG-3",
        "id": "5f981c00b982f0755dbdc13d",
        "key": "ORG-3",
        "version": 133,
        "lastCommentUpdatedAt": "2020-12-13T13:18:22.965+0000",
        "pendingReplyFrom": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1134669289",
                "id": "Employee ID",
                "display": "First and Last name",
            }
        ],
        "summary": "Issue name",
        "statusStartTime": "2020-11-03T11:19:24.733+0000",
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/19904929",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "description": "Issue description",
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "previousStatusLastAssignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "createdAt": "2020-10-27T13:09:20.085+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/19904929",
                "id": "Employee ID",
                "display": "First and Last name",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "checklistItems": [
            {
                "id": "5fde5f0a1aee261dd3b62edb",
                "text": "<Item text>",
                "textHtml": "Item text in HTML format",
                "checked": True,
                "checklistItemType": "standard",
            }
        ],
        "votes": 0,
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "deadline": "2020-10-28",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/ORG",
            "id": "1",
            "key": "ORG",
            "display": "Startrack",
        },
        "updatedAt": "2020-12-19T20:14:02.648+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "needInfo",
            "display": "Need info",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/3",
            "id": "3",
            "key": "inProgress",
            "display": "In progress",
        },
        "favorite": False,
    }
    mocker.post(
        "https://api.tracker.yandex.net/v2/issues/ORG-3/checklistItems", payload=resp
    )
    r = await checklists.create(
        get_client,
        issue_id="ORG-3",
        data=checklists.ChecklistCreateRequest(
            text="<Item text>",
            checked=True,
            assignee=1134669209,
            deadline=checklists.ChecklistDeadline(
                date=datetime(2021, 5, 9), deadline_type="date"
            ),
        ),
    )
    assert isinstance(r, checklists.ChecklistCreateResponse)
    assert r.checklist_items
    assert isinstance(r.checklist_items, list)
    assert r.checklist_items[0].checked == True
    assert r.checklist_items[0].text == "<Item text>"


@pytest.mark.asyncio
async def test_get_checklist(mocker, get_client):
    resp = [
        {
            "id": "5fde5f0a1aee261dd3b62edb",
            "text": "пункт чеклиста",
            "textHtml": "текст пункта в формате HTML",
            "checked": False,
            "assignee": {
                "id": 1134669209,
                "display": "Имя Фамилия",
                "passportUid": 1134669209,
                "login": "user_login",
                "firstName": "Имя",
                "lastName": "Фамилия",
                "email": "user_login@example.com",
                "trackerUid": 1134669209,
            },
            "deadline": {
                "date": "2021-05-09T00:00:00.000+0000",
                "deadlineType": "date",
                "isExceeded": False,
            },
            "checklistItemType": "standard",
        }
    ]
    mocker.get(
        "https://api.tracker.yandex.net/v2/issues/TEST-1/checklistItems", payload=resp
    )
    r = await checklists.get(get_client, "TEST-1")
    assert all([isinstance(item, checklists.ChecklistParamsResponse) for item in r])
    assert r[0].deadline
    assert r[0].deadline.date
    assert isinstance(r[0].deadline.date, datetime)


@pytest.mark.asyncio
async def test_edit_checklist(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/ORG-3",
        "id": "5f981c00b982f0755dbdc13d",
        "key": "ORG-3",
        "version": 184,
        "lastCommentUpdatedAt": "2021-02-06T17:14:22.965+0000",
        "pendingReplyFrom": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1134669289",
                "id": "employee ID",
                "display": "First and Last Name",
            }
        ],
        "summary": "Issue name",
        "statusStartTime": "2020-11-03T11:19:24.733+0000",
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/19904929",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "checklistDone": "2",
        "description": "Issue description",
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "previousStatusLastAssignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "createdAt": "2020-10-27T13:09:20.085+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/19904929",
                "id": "employee ID",
                "display": "First and Last Name",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "checklistItems": [
            {
                "id": "5fde5f0a1aee261dd3b62edb",
                "text": "Checklist item",
                "textHtml": "Item text in HTML format",
                "checked": False,
                "assignee": {
                    "id": 1134669209,
                    "display": "First and Last Name",
                    "passportUid": 1134669209,
                    "login": "user_login",
                    "firstName": "First name",
                    "lastName": "Last name",
                    "email": "user_login@example.com",
                    "trackerUid": 1134669209,
                },
                "deadline": {
                    "date": "2021-05-09T00:00:00.000+0000",
                    "deadlineType": "date",
                    "isExceeded": False,
                },
                "checklistItemType": "standard",
            },
        ],
        "checklistTotal": 4,
        "votes": 0,
        "deadline": "2020-10-28",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/ORG",
            "id": "1",
            "key": "ORG",
            "display": "Startrek",
        },
        "updatedAt": "2021-02-16T08:28:41.095+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "needInfo",
            "display": "Need info",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/3",
            "id": "3",
            "key": "inProgress",
            "display": "In progress",
        },
        "favorite": False,
    }
    mocker.patch(
        "https://api.tracker.yandex.net/v2/issues/ORG-3/checklistItems/5fde5f0a1aee261dd3b62edb",
        payload=resp,
    )
    r = await checklists.edit(
        get_client,
        "ORG-3",
        "5fde5f0a1aee261dd3b62edb",
        data=checklists.ChecklistEditRequest(text="TestEditMethod"),
    )
    assert isinstance(r, checklists.ChecklistEditResponse)
    assert r.checklist_items
    assert isinstance(r.checklist_items, list)


@pytest.mark.asyncio
async def test_delete_checklist_item(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/ORG-3",
        "id": "5f981c00b982f0755dbdc13d",
        "key": "ORG-3",
        "version": 151,
        "lastCommentUpdatedAt": "2020-12-13T13:18:22.965+0000",
        "pendingReplyFrom": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1134669289",
                "id": "employee ID",
                "display": "First and Last Name",
            }
        ],
        "summary": "Issue name",
        "statusStartTime": "2020-11-03T11:19:24.733+0000",
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/19904929",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "checklistDone": "0",
        "project": {
            "self": "https://api.tracker.yandex.net/v2/projects/7",
            "id": "7",
            "display": "Project name",
        },
        "description": "Issue description",
        "boards": [{"id": 14}],
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "previousStatusLastAssignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "createdAt": "2020-10-27T13:09:20.085+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/19904929",
                "id": "employee ID",
                "display": "First and Last Name",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "checklistItems": [
            {
                "id": "5fde5f0a1aee261dd3b62edb",
                "text": "checklist item",
                "textHtml": "item text in HTML format",
                "checked": False,
                "assignee": {
                    "id": 1134669209,
                    "display": "First and Last Name",
                    "passportUid": 1134669209,
                    "login": "user_login",
                    "firstName": "First name",
                    "lastName": "Last name",
                    "email": "user_login@example.com",
                    "trackerUid": 1134669209,
                },
                "deadline": {
                    "date": "2021-05-09T00:00:00.000+0000",
                    "deadlineType": "date",
                    "isExceeded": False,
                },
                "checklistItemType": "standard",
            },
        ],
        "checklistTotal": 4,
        "votes": 0,
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "employee ID",
            "display": "First and Last Name",
        },
        "deadline": "2020-10-28",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/ORG",
            "id": "1",
            "key": "ORG",
            "display": "Startrack",
        },
        "updatedAt": "2021-02-16T08:28:41.095+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "needInfo",
            "display": "Need info",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/3",
            "id": "3",
            "key": "inProgress",
            "display": "In progress",
        },
        "favorite": False,
    }
    mocker.delete(
        "https://api.tracker.yandex.net/v2/issues/ORG-3/checklistItems/5fde5f0a1aee261dd3b62edc",
        payload=resp,
    )
    r = await checklists.remove_item(
        get_client,
        "ORG-3",
        checklist_item_id="5fde5f0a1aee261dd3b62edc",
    )
    assert isinstance(r, checklists.ChecklistItemRemoveResponse)


@pytest.mark.asyncio
async def test_delete_checklist(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/ORG-3",
        "id": "5f981c00b982f0755dbdc13d",
        "key": "ORG-3",
        "version": 147,
        "lastCommentUpdatedAt": "2020-12-13T13:18:22.965+0000",
        "pendingReplyFrom": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1134669289",
                "id": "Employee ID",
                "display": "First and Last name",
            }
        ],
        "summary": "Issue name",
        "statusStartTime": "2020-11-03T11:19:24.733+0000",
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/19904929",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "checklistDone": "0",
        "description": "Issue description",
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "previousStatusLastAssignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "createdAt": "2020-10-27T13:09:20.085+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/19904929",
                "id": "Employee ID",
                "display": "First and Last name",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "checklistTotal": 4,
        "votes": 0,
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1134669289",
            "id": "Employee ID",
            "display": "First and Last name",
        },
        "deadline": "2020-10-28",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/ORG",
            "id": "1",
            "key": "ORG",
            "display": "Startrack",
        },
        "updatedAt": "2021-02-16T08:28:41.095+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "needInfo",
            "display": "Need info",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/3",
            "id": "3",
            "key": "inProgress",
            "display": "In progress",
        },
        "favorite": False,
    }
    mocker.delete(
        "https://api.tracker.yandex.net/v2/issues/ORG-3/checklistItems", payload=resp
    )
    r = await checklists.remove(get_client, "ORG-3")
    assert isinstance(r, checklists.ChecklistRemoveResponse)
    assert not getattr(r, "checklist_items", None)
