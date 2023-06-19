from typing import List

from ..base import BaseClient
from .models import *

ENDPOINT = "queues"


async def create(client: BaseClient, data: QueueRequest) -> QueueResponse:
    """
    create https://cloud.yandex.com/en/docs/tracker/concepts/queues/create-queue

    :param client: client instance
    :type client: BaseClient
    :param data: request body
    :type data: QueueRequest
    :return: response data
    :rtype: QueueResponse
    """
    url = f"{ENDPOINT}"
    response = await client.post(url, data)
    response_data = await response.json()
    response.close()
    return QueueResponse.parse_obj(response_data)


async def get(
    client: BaseClient,
    queue_id: str,
    expand_all: bool = False,
    expand_projects: bool = False,
    expand_components: bool = False,
    expand_versions: bool = False,
    expand_types: bool = False,
    expand_team: bool = False,
    expand_workflows: bool = False,
    expand_fields: bool = False,
    expand_issue_type_config: bool = False,
) -> QueueResponse:
    """
    get https://cloud.yandex.com/en/docs/tracker/concepts/queues/get-queue

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param expand_all: expand all attributes, defaults to False
    :type expand_all: bool, optional
    :param expand_projects: defaults to False
    :type expand_projects: bool, optional
    :param expand_components: defaults to False
    :type expand_components: bool, optional
    :param expand_versions: defaults to False
    :type expand_versions: bool, optional
    :param expand_types: defaults to False
    :type expand_types: bool, optional
    :param expand_team: defaults to False
    :type expand_team: bool, optional
    :param expand_workflows: defaults to False
    :type expand_workflows: bool, optional
    :param expand_fields: defaults to False
    :type expand_fields: bool, optional
    :param expand_issue_type_config: defaults to False
    :type expand_issue_type_config: bool, optional
    :return: response data
    :rtype: QueueResponse
    """
    url = f"{ENDPOINT}/{queue_id}"
    params = {}
    if expand_all:
        params["expand"] = "all"
    if expand_projects:
        params["expand"] = "projects"
    if expand_components:
        params["expand"] = "components"
    if expand_versions:
        params["expand"] = "versions"
    if expand_types:
        params["expand"] = "types"
    if expand_team:
        params["expand"] = "team"
    if expand_workflows:
        params["expand"] = "workflows"
    if expand_fields:
        params["expand"] = "fields"
    if expand_issue_type_config:
        params["expand"] = "issueTypeConfig"
    response = await client.get(url, params=params)
    response_data = await response.json()
    response.close()
    return QueueResponse.parse_obj(response_data)


async def list(
    client: BaseClient,
    expand_projects: bool = False,
    expand_components: bool = False,
    expand_versions: bool = False,
    expand_types: bool = False,
    expand_team: bool = False,
    expand_workflows: bool = False,
) -> List[QueueResponse]:
    """
    list https://cloud.yandex.com/en/docs/tracker/concepts/queues/get-queues

    :param client: client instance
    :type client: BaseClient
    :param expand_projects: defaults to False
    :type expand_projects: bool, optional
    :param expand_components: defaults to False
    :type expand_components: bool, optional
    :param expand_versions: defaults to False
    :type expand_versions: bool, optional
    :param expand_types: defaults to False
    :type expand_types: bool, optional
    :param expand_team: defaults to False
    :type expand_team: bool, optional
    :param expand_workflows:  defaults to False
    :type expand_workflows: bool, optional
    :return: response data
    :rtype:
    """
    url = f"{ENDPOINT}"
    params = {}
    if expand_projects:
        params["expand"] = "projects"
    if expand_components:
        params["expand"] = "components"
    if expand_versions:
        params["expand"] = "versions"
    if expand_types:
        params["expand"] = "types"
    if expand_team:
        params["expand"] = "team"
    if expand_workflows:
        params["expand"] = "workflows"
    response = await client.get(url, params)
    response_data = await response.json()
    response.close()
    return [QueueResponse.parse_obj(item) for item in response_data]


async def versions(client: BaseClient, queue_id: str) -> List[QueueVersionResponse]:
    """
    versions https://cloud.yandex.com/en/docs/tracker/concepts/queues/get-versions

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :return: response data
    :rtype: List[QueueVersionResponse]
    """
    url = f"{ENDPOINT}/{queue_id}/versions"
    response = await client.get(url)
    response_data = await response.json()
    response.close()
    return [QueueVersionResponse.parse_obj(item) for item in response_data]


async def fields(client: BaseClient, queue_id: str) -> List[QueueFieldsResponse]:
    """
    fields https://cloud.yandex.com/en/docs/tracker/concepts/queues/get-fields

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :return: response data
    :rtype: List[QueueFieldsResponse]
    """
    url = f"{ENDPOINT}/{queue_id}/fields"
    response = await client.get(url)
    response_data = await response.json()
    response.close()
    return [QueueFieldsResponse.parse_obj(item) for item in response_data]


async def delete(client: BaseClient, queue_id: str):
    """
    delete https://cloud.yandex.com/en/docs/tracker/concepts/queues/delete-queue

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    """

    url = f"{ENDPOINT}/{queue_id}"
    response = await client.delete(url)
    response.close()


async def restore(client: BaseClient, queue_id: str):
    """
    restore https://cloud.yandex.com/en/docs/tracker/concepts/queues/restore-queue

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    """

    url = f"{ENDPOINT}/{queue_id}/_restore"
    response = await client.post(url, data=None)
    response_data = await response.json()
    response.close()
    return QueueResponse.parse_obj(response_data)


async def remove_tags(client: BaseClient, queue_id: str, data: QueueTagsRequest):
    """
    remove_tags https://cloud.yandex.com/en/docs/tracker/concepts/queues/delete-tag

    :param client: client instance
    :type client: BaseClient
    :param data: request body
    :type data: QueueTagsRequest
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    """
    url = f"{ENDPOINT}/{queue_id}/tags/_remove"
    response = await client.post(url, data=data)
    response.close()


async def create_auto_action(
    client: BaseClient, queue_id: str, data: QueueAutoActionRequest
) -> QueueAutoActionResponse:
    """
    auto_action https://cloud.yandex.com/en/docs/tracker/concepts/queues/create-autoaction

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param data: request body
    :type data: QueueAutoActionRequest
    :return: response data
    :rtype: QueueAutoActionResponse
    """
    url = f"{ENDPOINT}/queues/{queue_id}/autoactions"
    response = await client.post(url, data=data)
    response_data = await response.json()
    response.close()
    return QueueAutoActionResponse.parse_obj(response_data)


async def get_auto_action(
    client: BaseClient, queue_id: str, auto_action_id: str
) -> QueueAutoActionResponse:
    """
    auto_actions https://cloud.yandex.com/en/docs/tracker/concepts/queues/get-autoaction

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param auto_action_id: e.g. AutoactionName
    :type auto_action_id: str
    :return: response body
    :rtype: QueueAutoActionResponse
    """
    url = f"{ENDPOINT}/queues/{queue_id}/autoactions/{auto_action_id}"
    response = await client.post(url=url, data=None)
    response_data = await response.json()
    response.close()
    return QueueAutoActionResponse.parse_obj(response_data)


async def create_trigger(
    client: BaseClient, queue_id: str, data: QueueTriggerRequest
) -> QueueTriggerResponse:
    """
    create_trigger https://cloud.yandex.com/en/docs/tracker/concepts/queues/create-trigger

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param data: request body
    :type data: QueueTriggerRequest
    :return: response data
    :rtype: QueueTriggerResponse
    """
    url = f"{ENDPOINT}/queues/{queue_id}/triggers"
    response = await client.post(url, data=data)
    response_data = await response.json()
    response.close()
    return QueueTriggerResponse.parse_obj(response_data)


async def get_trigger(
    client: BaseClient, queue_id: str, trigger_id: str
) -> QueueTriggerResponse:
    """
    get_trigger https://cloud.yandex.com/en/docs/tracker/concepts/queues/get-trigger

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param trigger_id: e.g. MyTrigger
    :type trigger_id: str
    :return: response data
    :rtype: QueueTriggerResponse
    """

    url = f"{ENDPOINT}/queues/{queue_id}/triggers/{trigger_id}"
    response = await client.get(url)
    response_data = await response.json()
    response.close()
    return QueueTriggerResponse.parse_obj(response_data)
