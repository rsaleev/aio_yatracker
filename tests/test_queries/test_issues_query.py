from aio_yatracker import tasks
from aio_yatracker.base import BaseClient
from tests.conftest import get_client


async def test_get_issue_parameters(get_client:BaseClient):
    r = await tasks.query.get_issues_parameters(get_client, "LOCKERS-441")
    assert isinstance(r, tasks.models.IssueParametersResponse)
