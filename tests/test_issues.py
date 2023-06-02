import re

import pytest

from aio_yatracker import issues
from aio_yatracker.common import *


@pytest.mark.asyncio
async def test_get_issue_parameters(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/TREK-9844",
        "id": "593cd211ef7e8a332414f2a7",
        "key": "TREK-9844",
        "version": 7,
        "lastCommentUpdatedAt": "2017-07-18T13:33:44.291+0000",
        "summary": "subtask",
        "parent": {
            "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2",
            "id": "593cd0acef7e8a332414f28e",
            "key": "JUNE-2",
            "display": "Task",
        },
        "aliases": ["JUNE-3"],
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "description": "<#<html><head></head><body><div>test</div><div>&nbsp;</div><div>&nbsp;</div> </body></html>#>",
        "sprint": [
            {
                "self": "https://api.tracker.yandex.net/v2/sprints/5317",
                "id": "5317",
                "display": "sprint1",
            }
        ],
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/2",
            "id": "2",
            "key": "normal",
            "display": "Medium",
        },
        "createdAt": "2017-06-11T05:16:01.339+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "votes": 0,
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/TREK",
            "id": "111",
            "key": "TREK",
            "display": "Startrack",
        },
        "updatedAt": "2017-07-18T13:33:44.291+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/1",
            "id": "1",
            "key": "open",
            "display": "Open",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "resolved",
            "display": "Resolved",
        },
        "favorite": False,
    }
    mocker.get(
        f"https://api.tracker.yandex.net/v2/issues/TREK-9844",
        payload=resp,
    )
    r = await issues.get(get_client, "TREK-9844")
    assert isinstance(r, issues.models.IssueParametersResponse)


@pytest.mark.asyncio
async def test_modify_issue(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/TREK-9844",
        "id": "593cd211ef7e8a332414f2a7",
        "key": "TREK-9844",
        "version": 7,
        "lastCommentUpdatedAt": "2017-07-18T13:33:44.291+0000",
        "summary": "subtask",
        "parent": {
            "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2",
            "id": "593cd0acef7e8a332414f28e",
            "key": "JUNE-2",
            "display": "Task",
        },
        "aliases": ["JUNE-3"],
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "description": "<#<html><head></head><body><div>test</div><div>&nbsp;</div><div>&nbsp;</div> </body></html>#>",
        "sprint": [
            {
                "self": "https://api.tracker.yandex.net/v2/sprints/5317",
                "id": "5317",
                "display": "sprint1",
            }
        ],
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/2",
            "id": "2",
            "key": "normal",
            "display": "Medium",
        },
        "createdAt": "2017-06-11T05:16:01.339+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "votes": 0,
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/TREK",
            "id": "111",
            "key": "TREK",
            "display": "Startrack",
        },
        "updatedAt": "2017-07-18T13:33:44.291+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/1",
            "id": "1",
            "key": "open",
            "display": "Open",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "resolved",
            "display": "Resolved",
        },
        "favorite": False,
    }
    """ 
    "parent": {
        "key": "TEST-2"},
    "sprint": [{"id": "3"}, {"id": "2"}],
    "followers": {
        "add": ["userlogin-1", "userlogin-2"]
        }
    """
    body = issues.IssueModificationRequest(
        parent=Attributes8(key="TEST-2"),
        sprint=[Attributes1(id="3"), Attributes1(id="2")],
        followers={"add": ["userlogin-1", "userlogin-2"]},
    )
    mocker.patch(
        f"https://api.tracker.yandex.net/v2/issues/TREK-9844",
        payload=resp,
    )
    r = await issues.modify(
        get_client,
        "TREK-9844",
        body,
    )
    assert isinstance(r, issues.models.IssueModificationResponse)


@pytest.mark.asyncio
async def test_create_issue(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/TREK-9844",
        "id": "593cd211ef7e8a332414f2a7",
        "key": "TREK-9844",
        "version": 7,
        "lastCommentUpdatedAt": "2017-07-18T13:33:44.291+0000",
        "summary": "subtask",
        "parent": {
            "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2",
            "id": "593cd0acef7e8a332414f28e",
            "key": "JUNE-2",
            "display": "Task",
        },
        "aliases": ["JUNE-3"],
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "description": "<#<html><head></head><body><div>test</div><div>&nbsp;</div><div>&nbsp;</div> </body></html>#>",
        "sprint": [
            {
                "self": "https://api.tracker.yandex.net/v2/sprints/5317",
                "id": "5317",
                "display": "sprint1",
            }
        ],
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/2",
            "id": "2",
            "key": "normal",
            "display": "Medium",
        },
        "createdAt": "2017-06-11T05:16:01.339+0000",
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "votes": 0,
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/TREK",
            "id": "111",
            "key": "TREK",
            "display": "Startrack",
        },
        "updatedAt": "2017-07-18T13:33:44.291+0000",
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/1",
            "id": "1",
            "key": "open",
            "display": "Open",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/2",
            "id": "2",
            "key": "resolved",
            "display": "Resolved",
        },
        "favorite": False,
    }
    body = issues.IssueCreationRequest(
        summary="Test issue",
        queue="Trek",
        parent="JUNE-2",
        type="bug",
        assignee="1120000000049224",
        attachment_ids=[55, 56],
    )
    mocker.post("https://api.tracker.yandex.net/v2/issues/", payload=resp)
    r = await issues.create(get_client, body)
    assert isinstance(r, issues.models.IssueCreationResponse)


@pytest.mark.asyncio
async def test_move_issue(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/NEW-1",
        "id": "1a2345678b",
        "key": "NEW-1",
        "version": 2,
        "aliases": ["TEST-1"],
        "previousQueue": {
            "self": "https://api.tracker.yandex.net/v2/queues/TEST",
            "id": "3",
            "key": "TEST",
            "display": "TEST",
        },
        "description": "<issue description>",
        "type": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Issue",
        },
        "createdAt": "2020-09-04T14:18:56.776+0000",
        "updatedAt": "2020-11-12T12:38:19.040+0000",
        "lastCommentUpdatedAt": "2020-10-18T13:33:44.291+0000",
        "summary": "Test",
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1234567890",
            "id": "1234567890",
            "display": "First and Last name",
        },
        "priority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "followers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1234567890",
                "id": "1234567890",
                "display": "First and Last name",
            }
        ],
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1234567890",
            "id": "1234567890",
            "display": "First and Last name",
        },
        "assignee": {
            "self": "https://api.tracker.yandex.net/v2/users/1234567890",
            "id": "1234567890",
            "display": "First and Last name",
        },
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/NEW",
            "id": "5",
            "key": "NEW",
            "display": "Queue",
        },
        "status": {
            "self": "https://api.tracker.yandex.net/v2/statuses/8",
            "id": "1",
            "key": "open",
            "display": "Open",
        },
        "previousStatus": {
            "self": "https://api.tracker.yandex.net/v2/statuses/1",
            "id": "1",
            "key": "open",
            "display": "Open",
        },
        "favorite": False,
    }
    mocker.post(
        "https://api.tracker.yandex.net/v2/issues/TEST-1/_move?queue=NEW", payload=resp
    )
    r = await issues.move(
        get_client,
        issue_id="TEST-1",
        dest_queue="NEW",
    )
    assert isinstance(r, issues.IssueMoveResponse)


@pytest.mark.asyncio
async def test_count_issues(mocker, get_client):
    resp = 5221186
    mocker.post("https://api.tracker.yandex.net/v2/issues/_count", payload=resp)
    r = await issues.count(
        get_client,
        issues.IssueCountRequest(filter={"queue": "JUNE", "assignee": "Empty()"}),
    )
    assert r == resp


@pytest.mark.asyncio
async def test_search_issues(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/issues/TREK-9844",
            "id": "593cd211ef7e8a332414f2a7",
            "key": "TREK-9844",
            "version": 7,
            "lastCommentUpdatedAt": "2017-07-18T13:33:44.291+0000",
            "summary": "subtask",
            "parent": {
                "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2",
                "id": "593cd0acef7e8a332414f28e",
                "key": "JUNE-2",
                "display": "Task",
            },
            "aliases": ["JUNE-3"],
            "updatedBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "description": "<#<html><head></head><body><div>test</div><div>&nbsp;</div><div>&nbsp;</div> </body></html>#>",
            "sprint": [
                {
                    "self": "https://api.tracker.yandex.net/v2/sprints/5317",
                    "id": "5317",
                    "display": "sprint1",
                }
            ],
            "type": {
                "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
                "id": "2",
                "key": "task",
                "display": "Issue",
            },
            "priority": {
                "self": "https://api.tracker.yandex.net/v2/priorities/2",
                "id": "2",
                "key": "normal",
                "display": "Medium",
            },
            "createdAt": "2017-06-11T05:16:01.339+0000",
            "followers": [
                {
                    "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                    "id": "<employee ID>",
                    "display": "<employee name displayed>",
                }
            ],
            "createdBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "votes": 0,
            "assignee": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "queue": {
                "self": "https://api.tracker.yandex.net/v2/queues/TREK",
                "id": "111",
                "key": "TREK",
                "display": "Startrack",
            },
            "updatedAt": "2017-07-18T13:33:44.291+0000",
            "status": {
                "self": "https://api.tracker.yandex.net/v2/statuses/1",
                "id": "1",
                "key": "open",
                "display": "Open",
            },
            "previousStatus": {
                "self": "https://api.tracker.yandex.net/v2/statuses/2",
                "id": "2",
                "key": "resolved",
                "display": "Resolved",
            },
            "favorite": False,
        }
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/issues/_search)(\?page=\d*&perPage=50)?"
    )
    mocker.post(pattern, payload=resp, repeat=True)
    async for issues_list in issues.search(
        get_client,
        data=issues.IssueSearchRequest(filter={"queue": "TREK"}),
    ):
        assert all(
            isinstance(issue, issues.IssueSearchResponse) for issue in issues_list
        )


@pytest.mark.asyncio
async def test_priorities(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/priorities/5",
            "id": 5,
            "key": "blocker",
            "version": 1341632717561,
            "name": "Блокер",
            "order": 5,
        },
    ]
    pattern = re.compile(
        r"https://api.tracker.yandex.net/v2/priorities(\?page=1&perPage=50)?"
    )
    mocker.get(
        pattern,
        payload=resp,
        repeat=True,
    )
    async for priorities_list in issues.priorities(get_client):
        assert all(
            isinstance(priority, issues.IssuePrioritiesResponse)
            for priority in priorities_list
        )


@pytest.mark.asyncio
async def test_transitions(mocker, get_client):
    resp = [
        {
            "id": "resolve",
            "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2/transitions/resolve",
            "display": "Resolve",
            "to": {
                "self": "https://api.tracker.yandex.net/v2/statuses/1",
                "id": "1",
                "key": "open",
                "display": "Open",
            },
        },
    ]
    pattern = re.compile(
        r"https://api.tracker.yandex.net/v2/issues/JUNE-2/transitions(\?page=1&perPage=50)?"
    )
    mocker.get(
        pattern,
        payload=resp,
        repeat=True,
    )
    async for transitions_list in issues.transitions(get_client, "JUNE-2"):
        assert all(
            isinstance(transition, issues.IssueTransitionResponse)
            for transition in transitions_list
        )


@pytest.mark.asyncio
async def test_transition(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/issues/DESIGN-1/transitions/close",
            "id": "close",
            "to": {
                "self": "https://api.tracker.yandex.net/v2/statuses/3",
                "id": "3",
                "key": "closed",
                "display": "Closed",
            },
            "screen": {
                "self": "https://api.tracker.yandex.net/v2/screens/50c85b17e4b04b38ef31a522",
                "id": "50c85b17e4b04b38ef31a522",
            },
        },
    ]
    mocker.post(
        "https://api.tracker.yandex.net/v2/issues/DESIGN-1/transitions/close/_execute",
        payload=resp,
    )
    r = await issues.transition(get_client, "DESIGN-1", "close")
    for status in r:
        assert isinstance(status, issues.IssueTransitionOperationResponse)


@pytest.mark.asyncio
async def test_changelog(mocker, get_client):
    resp = [
        {
            "id": "6033f986bd6c4a042c688392",
            "self": "https://api.tracker.yandex.net/v2/issues/TEST-27/changelog/6033f986bd6c4a042c688392",
            "issue": {
                "self": "https://api.tracker.yandex.net/v2/issues/TEST-27",
                "id": "6033f986bd6c4a042c688392",
                "key": "TEST-27",
                "display": "Issue name",
            },
            "updatedAt": "2021-02-22T18:35:50.157+0000",
            "updatedBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1234567890",
                "id": "1234567890",
                "display": "First and Last name",
            },
            "type": "IssueCreated",
            "transport": "front",
            "fields": [
                {
                    "field": {
                        "self": "https://api.tracker.yandex.net/v2/fields/status",
                        "id": "status",
                        "display": "Status",
                    },
                    "from": None,
                    "to": {
                        "self": "https://api.tracker.yandex.net/v2/statuses/1",
                        "id": "1",
                        "key": "open",
                        "display": "Open",
                    },
                }
            ],
        },
        {
            "id": "6033f98d4417c101b655b93b",
            "self": "https://api.tracker.yandex.net/v2/issues/TEST-27/changelog/6033f98d4417c101b655b93b",
            "issue": {
                "self": "https://api.tracker.yandex.net/v2/issues/TEST-27",
                "id": "6033f986bd6c4a042c688391",
                "key": "TEST-27",
                "display": "Issue name",
            },
            "updatedAt": "2021-02-22T18:35:57.359+0000",
            "updatedBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1234567890",
                "id": "1234567890",
                "display": "First and Last name",
            },
            "type": "IssueUpdated",
            "transport": "front",
            "fields": [
                {
                    "field": {
                        "self": "https://api.tracker.yandex.net/v2/fields/followers",
                        "id": "followers",
                        "display": "Followers",
                    },
                    "from": None,
                    "to": [
                        {
                            "self": "https://api.tracker.yandex.net/v2/users/1234567890",
                            "id": "1234567890",
                            "display": "First and Last name",
                        }
                    ],
                }
            ],
        },
        {
            "id": "6033f9954417c101b655b940",
            "self": "https://api.tracker.yandex.net/v2/issues/TEST-27/changelog/6033f9954417c101b655b940",
            "issue": {
                "self": "https://api.tracker.yandex.net/v2/issues/TEST-27",
                "id": "6033f986bd6c4a042c688391",
                "key": "TEST-27",
                "display": "Issue name",
            },
            "updatedAt": "2021-02-22T18:36:05.553+0000",
            "updatedBy": {
                "self": "https://api.tracker.yandex.net/v2/users/1234567890",
                "id": "1234567890",
                "display": "First and Last name",
            },
            "type": "IssueUpdated",
            "transport": "front",
            "fields": [
                {
                    "field": {
                        "self": "https://api.tracker.yandex.net/v2/fields/tags",
                        "id": "tags",
                        "display": "Tags",
                    },
                    "from": None,
                    "to": ["New tag"],
                }
            ],
        },
    ]
    pattern = re.compile(
        r"https://api.tracker.yandex.net/v2/issues/TEST-27/changelog(\?page=1&perPage=50)?"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for changelog in issues.changelog(get_client, "TEST-27"):
        assert all(
            [
                isinstance(changes, issues.IssueChangelogResponse)
                for changes in changelog
            ]
        )


@pytest.mark.asyncio
async def test_link_create(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/issues/TEST-1/links/1048570",
        "id": 1048570,
        "type": {
            "self": "https://api.tracker.yandex.net/v2/linktypes/relates",
            "id": "relates",
            "inward": "relates",
            "outward": "relates",
        },
        "direction": "inward",
        "object": {
            "self": "https://api.tracker.yandex.net/v2/issues/STARTREK-2",
            "id": "4ff3e8dae4b0e2ac27f6eb43",
            "key": "TREK-2",
            "display": "NEW!!!",
        },
        "createdBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000004859",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "updatedBy": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "createdAt": "2014-06-18T12:06:02.401+0000",
        "updatedAt": "2014-06-18T12:06:02.401+0000",
    }
    mocker.post("https://api.tracker.yandex.net/v2/issues/TEST-1/links", payload=resp)
    r = await issues.link(
        get_client,
        issue_id="TEST-1",
        data=issues.IssueRelationshipCreateRequest(
            relationship=Relationship.RELATES, issue="TREK-2"
        ),
    )
    assert isinstance(r, issues.IssueRelationshipCreateResponse)


@pytest.mark.asyncio
async def test_links(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/issues/JUNE-2/links/4709605",
            "id": 4709605,
            "type": {
                "self": "https://api.tracker.yandex.net/v2/linktypes/subtask",
                "id": "subtask",
                "inward": "Sub-issue",
                "outward": "Parent issue",
            },
            "direction": "outward",
            "object": {
                "self": "https://api.tracker.yandex.net/v2/issues/TREK-9844",
                "id": "593cd211ef7e8a332414f2a7",
                "key": "TREK-9844",
                "display": "subtask",
            },
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
            "createdAt": "2017-06-11T05:16:01.421+0000",
            "updatedAt": "2017-06-11T05:16:01.421+0000",
            "assignee": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000049224",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "status": {
                "self": "https://api.tracker.yandex.net/v2/statuses/1",
                "id": "1",
                "key": "open",
                "display": "Open",
            },
        }
    ]
    pattern = re.compile(
        r"https://api.tracker.yandex.net/v2/issues/JUNE-2/links(\?page=1&perPage=50)?"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for link in issues.links(get_client, "JUNE-2"):
        assert all(
            [isinstance(item, issues.IssueRelationshipResponse) for item in link]
        )


@pytest.mark.asyncio
async def test_link_remove(mocker, get_client):
    mocker.delete(
        "https://api.tracker.yandex.net/v2/issues/JUNE-2/links/4709605", status=204
    )
    await issues.unlink(get_client, "JUNE-2", "4709605")
