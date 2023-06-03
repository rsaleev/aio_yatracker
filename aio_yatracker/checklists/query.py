from typing import List

from ..base import BaseClient
from .models import *

ENDPOINT = "issues"


async def create(
    client: BaseClient, issue_id: str, data: ChecklistCreateRequest
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
    url = f"{ENDPOINT}/{issue_id}/checklistItems"
    response = await client.post(url=url, data=data)
    response_data = await response.json()
    response.close()
    return ChecklistCreateResponse.parse_obj(response_data)


async def get(client: BaseClient, issue_id: str) -> List[ChecklistParamsResponse]:
    """
    get checklist https://cloud.yandex.ru/docs/tracker/concepts/issues/get-checklist

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :return: response data
    :rtype: ChecklistParamsResponse
    """
    url = f"{ENDPOINT}/{issue_id}/checklistItems"
    response = await client.get(url=url)
    response_data = await response.json()
    response.close()
    return [ChecklistParamsResponse.parse_obj(item) for item in response_data]


async def edit(
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
    url = f"{ENDPOINT}/{issue_id}/checklistItems/{checklist_item_id}"
    response = await client.patch(url=url, data=data)
    response_data = await response.json()
    response.close()
    return ChecklistEditResponse.parse_obj(response_data)


async def remove(client: BaseClient, issue_id: str) -> ChecklistRemoveResponse:
    """
    remove_checklist https://cloud.yandex.ru/docs/tracker/concepts/issues/delete-checklist

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :return: response data
    :rtype: ChecklistRemoveResponse
    """
    url = f"{ENDPOINT}/{issue_id}/checklistItems"
    response = await client.delete(url=url)
    response_data = await response.json()
    response.close()
    return ChecklistRemoveResponse.parse_obj(response_data)


async def remove_item(
    client: BaseClient, issue_id: str, checklist_item_id: str
) -> ChecklistItemRemoveResponse:
    """
    remove checklist_item https://cloud.yandex.ru/docs/tracker/concepts/issues/delete-checklist-item

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param checklist_item_id: 5f981c00b982f0755dbdc13d
    :type checklist_item_id: str
    :return: response data
    :rtype: ChecklistItemRemoveResponse
    """
    url = f"{ENDPOINT}/{issue_id}/checklistItems/{checklist_item_id}"
    response = await client.delete(url=url)
    response_data = await response.json()
    response.close()
    return ChecklistItemRemoveResponse.parse_obj(response_data)
