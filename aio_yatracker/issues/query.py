from typing import Any, AsyncGenerator, Dict, List

from ..base import BaseClient, RequestParams
from ..common import ChangeType
from .models import *

ENDPOINT = "issues"


async def get(client: BaseClient, issue_id: str) -> IssueParametersResponse:
    """
    get issue https://cloud.yandex.com/en/docs/tracker/concepts/issues/get-issue

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :raises ClientError, ClientConnectionError
    :return: response data
    :rtype: IssueParametersResponse
    """
    url = f"{ENDPOINT}/{issue_id}"
    response = await client.get(url)
    response_data = await response.json()
    response.close()
    return IssueParametersResponse.parse_obj(response_data)


async def modify(
    client: BaseClient, issue_id: str, data: IssueModificationRequest
) -> IssueModificationResponse:
    """
    edit issue https://cloud.yandex.ru/docs/tracker/concepts/issues/patch-issue

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. "QUEUE-1"
    :type issue_id: str
    :param data: request body
    :type data: IssueModificationRequest
    :raises ClientError
    :raises ClientConnectionError
    :return: Add notes about how to use the system.response data
    :rtype: IssueModificationResponse
    """
    url = f"{ENDPOINT}/{issue_id}"
    response = await client.patch(url=url, data=data)
    response_data = await response.json()
    response.close()
    return IssueModificationResponse.parse_obj(response_data)


async def create(
    client: BaseClient, data: IssueCreationRequest
) -> IssueCreationResponse:
    """
    create issue https://cloud.yandex.ru/docs/tracker/concepts/issues/create-issue

    :param client: client instance
    :type client: BaseClient
    :param data: request body
    :type data: IssueModel
    :raises ClientError
    :raises ClientConnectionError
    :return: response data
    :rtype: IssueCreationResponse
    """
    url = f"{ENDPOINT}/"
    response = await client.post(url=url, data=data)
    response_data = await response.json()
    response.close()
    return IssueCreationResponse.parse_obj(response_data)


async def move(
    client: BaseClient,
    issue_id: str,
    dest_queue: str,
    data: IssueMoveRequest | None = None,
    notify: bool = True,
    notify_author: bool = False,
    move_all_fields: bool = False,
    initial_status: bool = False,
    expand_attachments: bool = False,
    expand_comments: bool = False,
    expand_workflow: bool = False,
    expand_transitions: bool = False,
) -> IssueMoveResponse:
    """
    move_issue https://cloud.yandex.ru/docs/tracker/concepts/issues/move-issue

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param dest_queue: e.g. NEW
    :type dest_queue: str
    :param data: see documentation, defaults to None
    :type data: IssueMoveRequest | None, optional
    :param notify: notify that issue was moved, defaults to True
    :type notify: bool, optional
    :param notify_author: notify author that issue was moved, defaults to False
    :type notify_author: bool, optional
    :param move_all_fields: move all fields, defaults to False
    :type move_all_fields: bool, optional
    :param initial_status: reset initial status to queue workflow default state, defaults to False
    :type initial_status: bool, optional
    :param expand_attachments: expand response data with attachments, defaults to False
    :type expand_attachments: bool, optional
    :param expand_comments: expand response data with comments, defaults to False
    :type expand_comments: bool, optional
    :param expand_workflow: expand response data with workflow, defaults to False
    :type expand_workflow: bool, optional
    :param expand_transitions: expand response data with transitions, defaults to False
    :type expand_transitions: bool, optional
    :raises ClientError
    :raises ClientConnectionError
    :return: response data
    :rtype: IssueMoveResponse
    """
    params: Dict[str, Any] = {
        "queue": dest_queue,
    }
    if not notify:  # true by default
        params["notify"] = "false"
    if notify_author:
        params["notify_author"] = "true"
    if move_all_fields:
        params["move_all_fields"] = "true"
    if initial_status:
        params["initial_status"] = "true"
    if expand_attachments:
        params["expand"] = "attachments"
    if expand_comments:
        params["expand"] = "comments"
    if expand_workflow:
        params["expand"] = "workflow"
    if expand_transitions:
        params["expand"] = "transitions"
    url = f"{ENDPOINT}/{issue_id}/_move"
    response = await client.post(url=url, data=data, params=params)
    response_data = await response.json()
    response.close()
    return IssueMoveResponse.parse_obj(response_data)


async def count(client: BaseClient, data: IssueCountRequest) -> int:
    """
    count_issues https://cloud.yandex.ru/docs/tracker/concepts/issues/count-issues

    :param client: client instance
    :type client: BaseClient
    :param data: request body
    :type data: IssueCountRequest
    :raises ClientError
    :raises ClientConnectionError
    :return: response data
    :rtype: int
    """
    url = f"{ENDPOINT}/_count"
    response = await client.post(url=url, data=data)
    response_data = int(await response.text())
    response.close()
    return response_data


async def search(client: BaseClient, data: IssueSearchRequest) -> AsyncGenerator:
    """
    search_issues get_issues_parametershttps://cloud.yandex.ru/docs/tracker/concepts/issues/search-issues

    :param client: client instance
    :type client: BaseClient
    :param data: request body
    :type data: IssueSearchRequest
    :rtype: AsyncGenerator
    :yield: List[IssueSearchResponse]
    :rtype: Iterator[AsyncGenerator]
    """
    url = f"{ENDPOINT}/_search"
    response = await client.post(url=url, data=data)
    response.close()
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i, per_page=50).dict(by_alias=True)
        paginated_response = await client.post(
            url=url, data=data, params=pagination_params
        )
        paginated_response_model = [
            IssueSearchResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def priorities(
    client: BaseClient, localized: bool = False
) -> AsyncGenerator[List[IssuePrioritiesResponse], None]:
    """
    get_priorities https://cloud.yandex.ru/docs/tracker/concepts/issues/get-priorities

    :param: localize response data
    :return: response data
    :yield: List[IssuePrioritiesResponse]
    :rtype: Iterator[AsyncGenerator[List[IssuePrioritiesResponse], None]]

    """
    url = f"priorities"
    params = RequestParams().dict(by_alias=True)
    if localized:
        params["localized"] = "true"
    response = await client.get(url=url, params=params)
    pagination = await client.handle_response(response)
    response.close()
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i)
        paginated_response = await client.get(
            url=url, params=pagination_params.dict(by_alias=True)
        )
        paginated_response_model = [
            IssuePrioritiesResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def transitions(
    client: BaseClient, issue_id: str
) -> AsyncGenerator[List[IssueTransitionResponse], None]:
    """
    get_transition https://cloud.yandex.ru/docs/tracker/concepts/issues/get-transitions

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :yield: List[IssueTransitionResponse]
    :rtype: Iterator[AsyncGenerator[List[IssueTransitionResponse], None]]
    """
    url = f"{ENDPOINT}/{issue_id}/transitions"
    response = await client.get(url=url)
    pagination = await client.handle_response(response)
    response.close()
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            IssueTransitionResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def transition(
    client: BaseClient,
    issue_id: str,
    transition_id: str,
    comments: str | None = None,
) -> List[IssueTransitionOperationResponse]:
    """
    change issue status https://cloud.yandex.ru/docs/tracker/concepts/issues/new-transition

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param transition_id: e.g. 1 or 'active'. See queue workflow configuration
    :type transition_id: str
    :param comments: comments to transition operation, defaults to None
    :type comments: str | None, optional
    :return: response data
    :rtype: IssueTransitionOperationResponse
    """
    url = f"{ENDPOINT}/{issue_id}/transitions/{transition_id}/_execute"
    params = None
    if comments:
        params = {"comments": comments}
    response = await client.post(url=url, data=None, params=params)
    response_data = await response.json()
    response.close()
    return [IssueTransitionOperationResponse.parse_obj(item) for item in response_data]


async def changelog(
    client: BaseClient,
    issue_id: str,
    changed_id: str | None = None,
    changed_field: str | None = None,
    changed_type: ChangeType | None = None,
) -> AsyncGenerator[List[IssueChangelogResponse], None]:
    """
    retrieve issue changelog https://cloud.yandex.ru/docs/tracker/concepts/issues/get-changelog

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param changed_id: id of change, defaults to None
    :type changed_id: str | None, optional
    :param changed_field: field that was changed, defaults to None
    :type changed_field: str | None, optional
    :param changed_type: type of change, defaults to None
    :type changed_type: ChangeType | None, optional
    :yield: List[IssueChangelogResponse]
    :rtype: Iterator[AsyncGenerator[List[IssueChangelogResponse], None]]
    """
    params = {}
    if changed_id:
        params["id"] = changed_id
    if changed_field:
        params["field"] = changed_field
    if changed_type:
        params["type"] = changed_type.value
    url = f"{ENDPOINT}/{issue_id}/changelog"
    response = await client.get(url=url, params=params)
    pagination = await client.handle_response(response)
    response.close()
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            IssueChangelogResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def link(
    client: BaseClient, issue_id: str, data: IssueRelationshipCreateRequest
) -> IssueRelationshipCreateResponse:
    """
    link issues https://cloud.yandex.ru/docs/tracker/concepts/issues/link-issue

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param data: request body
    :type data: IssueRelationshipOperationRequest
    :return: response data
    :rtype: IssueRelationshipCreateResponse
    """
    url = f"{ENDPOINT}/{issue_id}/links"
    response = await client.post(url=url, data=data)
    response_data = await response.json()
    response.close()
    return IssueRelationshipCreateResponse.parse_obj(response_data)


async def links(
    client: BaseClient, issue_id: str
) -> AsyncGenerator[List[IssueRelationshipResponse], None]:
    """
    retrieve links to issue https://cloud.yandex.ru/docs/tracker/concepts/issues/get-links

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :return: response data
    :yield: List[IssueRelationshipResponse]
    :rtype: Iterator[AsyncGenerator[List[IssueRelationshipResponse], None]]
    """
    url = f"{ENDPOINT}/{issue_id}/links"
    response = await client.get(url=url)
    pagination = await client.handle_response(response)
    response.close()
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            IssueRelationshipResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def unlink(client: BaseClient, issue_id: str, related_issue_id: str):
    """
    unlink issues https://cloud.yandex.ru/docs/tracker/concepts/issues/delete-link-issue

    :param client: client instance
    :type client: BaseClient
    :param issue_id: root issue id, e.q. QUEUE-1
    :type issue_id: str
    :param related_issue_id: e.g. QUEUE-1
    :type related_issue_id: str
    """

    url = f"{ENDPOINT}/{issue_id}/links/{related_issue_id}"
    response = await client.delete(url=url)
    response.close()
