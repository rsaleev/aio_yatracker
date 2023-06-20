import re

import pytest

from aio_yatracker import queues


@pytest.mark.asyncio
async def test_create_queue(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/queues/DESIGN",
        "id": 111,
        "key": "DESIGN",
        "version": 1400150916068,
        "name": "Design",
        "lead": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000004859",
            "id": "artemredkin",
            "display": "Artem Redkin",
        },
        "assignAuto": False,
        "allowExternals": False,
        "defaultType": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
            "id": "2",
            "key": "task",
            "display": "Task",
        },
        "defaultPriority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/2",
            "id": "2",
            "key": "normal",
            "display": "Normal",
        },
    }
    body = queues.QueueRequest(
        key="DESIGN",
        name="Design",
        lead="artemredkin",
        issues_types_config=queues.QueueIssueTypeConfig(
            issue_type="task", workflow="oicn", resolutions=["wontFix", "close"]
        ),
    )
    mocker.post(
        "https://api.tracker.yandex.net/v2/queues",
        payload=resp,
    )
    r = await queues.create(get_client, data=body)
    assert r.key == body.key
    assert r.lead.id == body.lead


@pytest.mark.asyncio
async def test_get_queue(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/queues/TEST",
        "id": 3,
        "key": "TEST",
        "version": 5,
        "name": "Test",
        "description": "Queue created for testing purposes",
        "lead": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "assignAuto": False,
        "defaultType": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
            "id": "1",
            "key": "bug",
            "display": "Bug",
        },
        "defaultPriority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "teamUsers": [
            {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
        ],
        "issueTypes": [
            {
                "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                "id": "1",
                "key": "bug",
                "display": "Bug",
            },
        ],
        "versions": [
            {
                "self": "https://api.tracker.yandex.net/v2/versions/4",
                "id": "4",
                "display": "Cuckoo",
            }
        ],
        "workflows": {
            "dev": [
                {
                    "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                    "id": "1",
                    "key": "bug",
                    "display": "Bug",
                },
            ]
        },
        "denyVoting": False,
        "issueTypesConfig": [
            {
                "issueType": {
                    "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                    "id": "1",
                    "key": "bug",
                    "display": "Bug",
                },
                "workflow": {
                    "self": "https://api.tracker.yandex.net/v2/workflows/dev",
                    "id": "dev",
                    "display": "dev",
                },
                "resolutions": [
                    {
                        "self": "https://api.tracker.yandex.net/v2/resolutions/2",
                        "id": "2",
                        "key": "wontFix",
                        "display": "Won't fix",
                    },
                ],
            },
        ],
    }
    mocker.get("https://api.tracker.yandex.net/v2/queues/TEST?expand=all", payload=resp)
    r = await queues.get(get_client, "TEST", expand_all=True)
    assert r.key == "TEST"
    assert r.issue_types_config
    assert r.issue_types_config[0].issue_type.key == "bug"


@pytest.mark.asyncio
async def test_list_queues(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/queues/TEST",
            "id": 3,
            "key": "TEST",
            "version": 5,
            "name": "Test",
            "description": "Queue created for testing purposes",
            "lead": {
                "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                "id": "<employee ID>",
                "display": "<employee name displayed>",
            },
            "assignAuto": False,
            "defaultType": {
                "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                "id": "1",
                "key": "bug",
                "display": "Bug",
            },
            "defaultPriority": {
                "self": "https://api.tracker.yandex.net/v2/priorities/3",
                "id": "3",
                "key": "normal",
                "display": "Medium",
            },
            "teamUsers": [
                {
                    "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
                    "id": "<employee ID>",
                    "display": "<employee name displayed>",
                },
            ],
            "issueTypes": [
                {
                    "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                    "id": "1",
                    "key": "bug",
                    "display": "Bug",
                },
            ],
            "versions": [
                {
                    "self": "https://api.tracker.yandex.net/v2/versions/4",
                    "id": "4",
                    "display": "Cuckoo",
                }
            ],
            "workflows": {
                "dev": [
                    {
                        "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                        "id": "1",
                        "key": "bug",
                        "display": "Bug",
                    },
                ]
            },
            "denyVoting": False,
            "issueTypesConfig": [
                {
                    "issueType": {
                        "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
                        "id": "1",
                        "key": "bug",
                        "display": "Bug",
                    },
                    "workflow": {
                        "self": "https://api.tracker.yandex.net/v2/workflows/dev",
                        "id": "dev",
                        "display": "dev",
                    },
                    "resolutions": [
                        {
                            "self": "https://api.tracker.yandex.net/v2/resolutions/2",
                            "id": "2",
                            "key": "wontFix",
                            "display": "Won't fix",
                        },
                    ],
                },
            ],
        },
    ]
    mocker.get("https://api.tracker.yandex.net/v2/queues", payload=resp)
    r = await queues.list(get_client)
    assert isinstance(r, list)
    assert all([isinstance(item, queues.QueueResponse) for item in r])


@pytest.mark.asyncio
async def test_queue_versions(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/versions/49650",
            "id": 49650,
            "version": 1,
            "queue": {
                "self": "https://api.tracker.yandex.net/v2/queues/JUNE",
                "id": "1928",
                "key": "JUNE",
                "display": "june",
            },
            "name": "version1",
            "description": "iohb ±!@#$%^&*()_+=-/\\?<>.,/§:»'|;",
            "startDate": "2017-06-09",
            "dueDate": "2017-06-09",
            "released": False,
            "archived": False,
        },
    ]
    mocker.get("https://api.tracker.yandex.net/v2/queues/TEST/versions", payload=resp)
    r = await queues.versions(get_client, "TEST")
    assert r


@pytest.mark.asyncio
async def test_queue_fields(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/fields/stand",
            "id": "stand",
            "name": "Bench",
            "version": 1361890459119,
            "schema": {"type": "string", "required": False},
            "readonly": False,
            "options": False,
            "suggest": False,
            "optionsProvider": {
                "type": "QueueFixedListOptionsProvider",
                "values": {
                    "DIRECT": [
                        "Not specified",
                        "Test",
                        "Development",
                        "Beta",
                        "Production",
                        "Trunk",
                    ]
                },
                "defaults": [
                    "Not specified",
                    "Test",
                    "Development",
                    "Beta",
                    "Production",
                ],
            },
            "queryProvider": {"type": "StringOptionalQueryProvider"},
            "order": 222,
        },
    ]
    mocker.get("https://api.tracker.yandex.net/v2/queues/TEST/fields", payload=resp)
    r = await queues.fields(get_client, "TEST")
    assert r


@pytest.mark.asyncio
async def test_delete_queue(mocker, get_client):
    mocker.delete("https://api.tracker.yandex.net/v2/queues/TEST")
    await queues.delete(get_client, "TEST")


@pytest.mark.asyncio
async def test_restore_queue(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/queues/TEST",
        "id": 3,
        "key": "TEST",
        "version": 5,
        "name": "Test",
        "lead": {
            "self": "https://api.tracker.yandex.net/v2/users/1120000000016876",
            "id": "<employee ID>",
            "display": "<employee name displayed>",
        },
        "assignAuto": False,
        "defaultType": {
            "self": "https://api.tracker.yandex.net/v2/issuetypes/1",
            "id": "1",
            "key": "bug",
            "display": "Error",
        },
        "defaultPriority": {
            "self": "https://api.tracker.yandex.net/v2/priorities/3",
            "id": "3",
            "key": "normal",
            "display": "Medium",
        },
        "denyVoting": False,
    }
    mocker.post("https://api.tracker.yandex.net/v2/queues/TEST/_restore", payload=resp)
    r = await queues.restore(get_client, "TEST")
    assert r.key == "TEST"


@pytest.mark.asyncio
async def test_remove_tag(mocker, get_client):
    mocker.post("https://api.tracker.yandex.net/v2/queues/TEST/tags/_remove")
    await queues.remove_tags(
        get_client, "TEST", data=queues.QueueTagsRequest(tag="test")
    )


@pytest.mark.asyncio
async def test_create_auto_action(mocker, get_client):
    resp = {
        "id": 9,
        "self": "https://api.tracker.yandex.net/v2/queues/DESIGN/autoactions/9",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/DESIGN",
            "id": "26",
            "key": "DESIGN",
            "display": "Design",
        },
        "name": "autoaction_name",
        "version": 1,
        "active": True,
        "created": "2022-01-21T17:10:22.993+0000",
        "updated": "2022-01-21T17:10:22.993+0000",
        "filter": {"assignee": ["1134669290"], "priority": ["critical"]},
        "actions": [
            {
                "type": "Transition",
                "id": 1,
                "status": {
                    "self": "https://api.tracker.yandex.net/v2/statuses/2",
                    "id": "2",
                    "key": "needInfo",
                    "display": "Need info",
                },
            }
        ],
        "enableNotifications": False,
        "totalIssuesProcessed": 0,
        "intervalMillis": 3600000,
        "calendar": {"id": 2},
    }
    mocker.post(
        "https://api.tracker.yandex.net/v2/queues/DESIGN/autoactions", payload=resp
    )
    body = queues.QueueAutoActionRequest(
        name="AutoactionName",
        filter={"priority": ["critical"], "status": ["inProgress"]},
        actions=[{"type": "Transition", "status": {"key": "needInfo"}}],
    )
    r = await queues.create_auto_action(get_client, "DESIGN", data=body)
    assert r


@pytest.mark.asyncio
async def test_auto_action_get(mocker, get_client):
    resp = {
        "id": 9,
        "self": "https://api.tracker.yandex.net/v2/queues/DESIGN/autoactions/9",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/DESIGN",
            "id": "26",
            "key": "DESIGN",
            "display": "Design",
        },
        "name": "autoaction_name",
        "version": 4,
        "active": True,
        "created": "2021-04-15T04:49:44.802+0000",
        "updated": "2022-01-26T16:29:05.356+0000",
        "filter": {"priority": ["critical"]},
        "actions": [
            {
                "type": "Transition",
                "id": 1,
                "status": {
                    "self": "https://api.tracker.yandex.net/v2/statuses/2",
                    "id": "2",
                    "key": "needInfo",
                    "display": "Need info",
                },
            }
        ],
        "enableNotifications": False,
        "lastLaunch": "2022-02-01T14:09:48.216+0000",
        "totalIssuesProcessed": 0,
        "intervalMillis": 3600000,
        "calendar": {"id": 2},
    }
    mocker.post(
        "https://api.tracker.yandex.net/v2/queues/DESIGN/autoactions/autoaction_name",
        payload=resp,
    )
    r = await queues.get_auto_action(get_client, "DESIGN", "autoaction_name")
    assert r.name == "autoaction_name"
    assert r.queue.key == "DESIGN"


@pytest.mark.asyncio
async def test_create_trigger(mocker, get_client):
    resp = {
        "id": 16,
        "self": "https://api.tracker.yandex.net/v2/queues/DESIGN/triggers/16",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/DESIGN",
            "id": "26",
            "key": "DESIGN",
            "display": "Design",
        },
        "name": "trigger_name",
        "order": "0.0002",
        "actions": [
            {
                "type": "Transition",
                "id": 1,
                "status": {
                    "self": "https://api.tracker.yandex.net/v2/statuses/2",
                    "id": "2",
                    "key": "needInfo",
                    "display": "Need info",
                },
            }
        ],
        "conditions": [
            {"type": "Or", "conditions": [{"type": "Event.comment-create"}]}
        ],
        "version": 1,
        "active": True,
    }
    mocker.post(
        "https://api.tracker.yandex.net/v2/queues/DESIGN/triggers", payload=resp
    )
    r = await queues.create_trigger(
        get_client,
        "DESIGN",
        data=queues.QueueTriggerRequest(
            name="TriggerName",
            actions=[{"type": "Transition", "status": {"key": "open"}}],
            conditions=[{"type": "CommentFullyMatchCondition", "word": "Open"}],
            active=False,
        ),
    )
    assert r


@pytest.mark.asyncio
async def test_get_trigger(mocker, get_client):
    resp = {
        "id": 16,
        "self": "https://api.tracker.yandex.net/v2/queues/DESIGN/triggers/16",
        "queue": {
            "self": "https://api.tracker.yandex.net/v2/queues/DESIGN",
            "id": "26",
            "key": "DESIGN",
            "display": "Design",
        },
        "name": "trigger_name",
        "order": "0.0002",
        "actions": [
            {
                "type": "Transition",
                "id": 1,
                "status": {
                    "self": "https://api.tracker.yandex.net/v2/statuses/2",
                    "id": "2",
                    "key": "needInfo",
                    "display": "Need info",
                },
            }
        ],
        "conditions": [
            {"type": "Or", "conditions": [{"type": "Event.comment-create"}]}
        ],
        "version": 1,
        "active": True,
    }
    mocker.get("https://api.tracker.yandex.net/v2/queues/DESIGN/triggers/trigger_name", payload=resp)
    r = await queues.get_trigger(get_client, 'DESIGN', 'trigger_name')
    assert r
    assert r.name == 'trigger_name'

