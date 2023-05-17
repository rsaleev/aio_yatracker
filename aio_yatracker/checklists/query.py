from typing import List

from ..base import BaseClient
from .models import *


class Query:
    def __init__(self):
        self._endpoint = "issues"

    async def create(
        self, client: BaseClient, issue_id: str, data: ChecklistCreateRequest
    ) -> ChecklistCreateResponse:
        """
        create https://cloud.yandex.ru/docs/tracker/concepts/issues/add-checklist-item

        :param client: client instance
        :type client: BaseClient
        :param issue_id: e.g. QUEUE-1
        :type issue_id: str
        :param data: request body
        :type data: ChecklistCreateRequest
        :return: response data
        :rtype: ChecklistCreateResponse
        """
        url = f"{self._endpoint}/{issue_id}/checklistItems"
        response = await client.post(url=url, data=data)
        response_data = await response.json()
        response.close()
        return ChecklistCreateResponse.parse_obj(response_data)

    async def get_checklist(
        self, client: BaseClient, issue_id: str
    ) -> List[ChecklistParamsResponse]:
        """
        get_checklist https://cloud.yandex.ru/docs/tracker/concepts/issues/get-checklist

        :param client: client instance
        :type client: BaseClient
        :param issue_id: e.g. QUEUE-1
        :type issue_id: str
        :return: response data
        :rtype: ChecklistParamsResponse
        """
        url = f"{self._endpoint}/{issue_id}/checklistItems"
        response = await client.get(url=url)
        response_data = await response.json()
        response.close()
        return [ChecklistParamsResponse.parse_obj(item) for item in response_data]

    async def edit_checklist(
        self,
        client: BaseClient,
        issue_id: str,
        checklist_item_id: str,
        data: ChecklistEditRequest,
    ) -> ChecklistEditResponse:
        """
        edit_checklist https://cloud.yandex.ru/docs/tracker/concepts/issues/edit-checklist

        :param client: client instance
        :type client: BaseClient
        :param issue_id: e.g. QUEUE-1
        :type issue_id: str
        :param checklist_item_id: e.g. 5fde5f0a1aee261dd3b62edb
        :type checklist_item_id: str
        :param data: request body
        :type data: ChecklistEditRequest
        :return: response data
        :rtype: ChecklistEditResponse
        """
        url = f"{self._endpoint}/{issue_id}/checklistItems/{checklist_item_id}"
        response = await client.patch(url=url, data=data)
        response_data = await response.json()
        response.close()
        return ChecklistEditResponse.parse_obj(response_data)

    async def remove_checklist(self, client: BaseClient, issue_id: str):
        """
        remove_checklist https://cloud.yandex.ru/docs/tracker/concepts/issues/delete-checklist

        :param client: client instance
        :type client: BaseClient
        :param issue_id: e.g. QUEUE-1
        :type issue_id: str
        """
        url = f"{self._endpoint}/{issue_id}/checklistItems"
        response = await client.delete(url=url)
        response.close()

    async def remove_checklist_item(
        self, client: BaseClient, issue_id: str, checklist_item_id: str
    ):
        """
        remove_checklist_item https://cloud.yandex.ru/docs/tracker/concepts/issues/delete-checklist-item

        :param client: client instance
        :type client: BaseClient
        :param issue_id: e.g. QUEUE-1
        :type issue_id: str
        :param checklist_item_id: 5f981c00b982f0755dbdc13d
        :type checklist_item_id: str
        """
        url = f"{self._endpoint}/{issue_id}/checklistItems/{checklist_item_id}"
        response = await client.delete(url=url)
        response.close()


query = Query()
