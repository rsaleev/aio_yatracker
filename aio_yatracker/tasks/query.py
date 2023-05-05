from aio_yatracker.base import BaseClient
from .models import IssueParametersResponse


class Query:

    def __init__(self):
        self._endpoint = "/issues"


    async def get_issues_parameters(self, client:BaseClient, issue_id:int):
        response = await client.get(url=f"{self._endpoint}/{issue_id}")
        if response:
            return IssueParametersResponse.parse_obj(response)
        return 