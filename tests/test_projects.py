import pytest

from aio_yatracker import projects
from aio_yatracker.base import BaseClient

@pytest.mark.asyncio
async def test_create_project(get_client: BaseClient, get_primary_queue_id: str):
    r = await projects.query.create(
        get_client,
        data=projects.ProjectCreateRequest(
            name="test_project", queues=get_primary_queue_id
        ),
    )
    assert isinstance(r, projects.ProjectCreateResponse)
