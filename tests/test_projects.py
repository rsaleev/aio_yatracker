from aio_yatracker import projects
from aio_yatracker.base import BaseClient

async def test_create_project(get_client):
    r = await projects.query.