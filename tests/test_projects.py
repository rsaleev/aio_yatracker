import re
from datetime import datetime

import pytest

from aio_yatracker import projects


@pytest.mark.asyncio
async def test_create_project(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/projects/9",
        "id": "9",
        "version": 1,
        "key": "Project",
        "name": "Project",
        "description": "New project",
        "lead": {
            "self": "https://api.tracker.yandex.net/v2/users/12314567890",
            "id": "1234567890",
            "display": "First and Last name",
        },
        "status": "launched",
        "startDate": "2020-11-16",
        "endDate": "2020-12-16",
    }
    mocker.post("https://api.tracker.yandex.net/v2/projects", payload=resp)
    r = await projects.create(
        get_client,
        data=projects.ProjectCreateRequest(name="Project", queues="TREK"),
    )
    assert isinstance(r, projects.ProjectCreateResponse)
    assert r.name == "Project"
    assert r.start_date == datetime(2020, 11, 16).date()
    assert r.end_date == datetime(2020, 12, 16).date()


@pytest.mark.asyncio
async def test_get_project_params(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/projects/9",
        "id": "9",
        "version": 1,
        "key": "Project",
        "name": "Project",
        "description": "New project",
        "lead": {
            "self": "https://api.tracker.yandex.net/v2/users/12314567890",
            "id": "1234567890",
            "display": "First and Last name",
        },
        "status": "launched",
        "startDate": "2020-11-16",
        "endDate": "2020-12-16",
    }
    mocker.get("https://api.tracker.yandex.net/v2/projects/9", payload=resp)
    r = await projects.get(get_client, "9")
    assert isinstance(r, projects.ProjectParamsResponse)
    assert r.id == "9"


@pytest.mark.asyncio
async def test_get_projects(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/projects/1",
            "id": "1",
            "version": 1,
            "key": "Project 1",
            "name": "Project 1",
            "description": "First project",
            "lead": {
                "self": "https://api.tracker.yandex.net/v2/users/12314567890",
                "id": "1234567890",
                "display": "First and Last name",
            },
            "status": "launched",
            "startDate": "2020-11-01",
            "endDate": "2020-12-01",
        },
        {
            "self": "https://api.tracker.yandex.net/v2/projects/2",
            "id": "2",
            "version": 1,
            "key": "Project 2",
            "name": "Project 2",
            "description": "Another project",
            "lead": {
                "self": "https://api.tracker.yandex.net/v2/users/12314567890",
                "id": "1234567890",
                "display": "First and Last name",
            },
            "status": "launched",
            "startDate": "2020-11-02",
            "endDate": "2020-12-02",
        },
    ]
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/projects)(\?expand=queues)?(&page=\d*&perPage=\d*)?$"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for projects_list in projects.list(get_client, queues=True):
        for project in projects_list:
            assert isinstance(project, projects.ProjectsResponse)
            assert "queues" in project.dict().keys()


@pytest.mark.asyncio
async def test_get_queues(mocker, get_client):
    resp = [
        {
            "self": "https://api.tracker.yandex.net/v2/queues/ORG",
            "id": 1,
            "key": "ORG",
            "version": 6,
            "name": "Default",
            "description": 'Queue description "Default" (ORG)',
            "lead": {
                "self": "https://api.tracker.yandex.net/v2/users/780889736",
                "id": "780889736",
                "display": "Tracker service robot ",
            },
            "assignAuto": False,
            "defaultType": {
                "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
                "id": "2",
                "key": "task",
                "display": "Issue",
            },
            "defaultPriority": {
                "self": "https://api.tracker.yandex.net/v2/priorities/3",
                "id": "3",
                "key": "normal",
                "display": "Medium",
            },
            "allowExternalMailing": True,
            "addIssueKeyInEmail": True,
            "denyVoting": False,
            "denyConductorAutolink": False,
            "denyTrackerAutolink": True,
            "useComponentPermissionsIntersection": False,
            "useLastSignature": False,
        },
        {
            "self": "https://api.tracker.yandex.net/v2/queues/TEST",
            "id": 3,
            "key": "TEST",
            "version": 8,
            "name": "Testing",
            "description": 'Description of the "Testing" queue (TEST)',
            "lead": {
                "self": "https://api.tracker.yandex.net/v2/users/1234567890",
                "id": "1234567890",
                "display": "First and Last name",
            },
            "assignAuto": False,
            "defaultType": {
                "self": "https://api.tracker.yandex.net/v2/issuetypes/2",
                "id": "2",
                "key": "task",
                "display": "Issue",
            },
            "defaultPriority": {
                "self": "https://api.tracker.yandex.net/v2/priorities/3",
                "id": "3",
                "key": "normal",
                "display": "Medium",
            },
            "allowExternalMailing": False,
            "addIssueKeyInEmail": False,
            "denyVoting": False,
            "denyConductorAutolink": False,
            "denyTrackerAutolink": False,
            "useComponentPermissionsIntersection": False,
            "useLastSignature": False,
        },
    ]

    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/projects/\d*/queues)(\?expand=\w*)?(&page=\d*&perPage=\d*)?$"
    )
    mocker.get(pattern, payload=resp, repeat=True)
    async for queues_list in projects.queues(get_client, "1", expand_all=True):
        for queue in queues_list:
            assert isinstance(queue, projects.ProjectQueueResponse)


@pytest.mark.asyncio
async def test_edit_project(mocker, get_client):
    resp = {
        "self": "https://api.tracker.yandex.net/v2/projects/9",
        "id": "9",
        "version": 5,
        "key": "Project",
        "name": "Project",
        "description": "Project with updates",
        "lead": {
            "self": "https://api.tracker.yandex.net/v2/users/12314567890",
            "id": "1234567890",
            "display": "First and Last name",
        },
        "status": "launched",
        "startDate": "2020-11-16",
        "endDate": "2020-12-16",
    }
    pattern = re.compile(
        r"(^https://api.tracker.yandex.net/v2/projects/9\?version=1)(expand=queues)?$"
    )
    mocker.put(pattern, payload=resp)
    r = await projects.edit(
        get_client,
        project_id="9",
        version=1,
        data=projects.ProjectEditRequest(queues="ORG", name="Project"),
    )
    assert isinstance(r, projects.ProjectEditResponse)


@pytest.mark.asyncio
async def test_delete_queues(mocker, get_client):
    mocker.delete("https://api.tracker.yandex.net/v2/projects/9")
    await projects.queries.delete(get_client, "9")

