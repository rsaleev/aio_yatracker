from typing import AsyncGenerator, List, Optional

from ..base import BaseClient, RequestParams
from .models import *

ENDPOINT = "issues"


async def add(
    client: BaseClient, issue_id: str, data: CommentCreateRequest
) -> CommentCreateResponse:
    """
    add comment https://cloud.yandex.com/en/docs/tracker/concepts/issues/add-comment
    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param text: e.g. "New comment"
    :type text: str
    :param attachments: e.g ['56',,57'], defaults to None
    :type attachments: typing.Optional[typing.List[str]], optional
    :param summonees: e.g. ['1234567', '1234568'], defaults to None
    :type summonees: typing.Optional[typing.List[str]], optional
    :param maillist: e.g. ['user1@yandex.ru', 'user2@yandex.ru'], defaults to None
    :type maillist: typing.Optional[typing.List[str]], optional
    :return: response data
    :rtype: CommentResponse
    """
    url = f"{ENDPOINT}/{issue_id}/comments"
    response = await client.post(url, data)
    response_data = await response.json()
    response.close()
    return CommentCreateResponse.parse_obj(response_data)


async def list(
    client: BaseClient,
    issue_id: str,
) -> AsyncGenerator:
    """
    list comments

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :yield: List[CommentResponse]
    :rtype: Iterator[AsyncGenerator]
    """
    url = f"{ENDPOINT}/{issue_id}/comments"
    response = await client.get(url)
    response.close()
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i, per_page=50).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            CommentListResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def edit(
    client: BaseClient,
    issue_id: str,
    comment_id:int,
    data: CommentEditRequest,
) -> CommentEditResponse:
    """
    edit comment

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param comment_id: e.g. 684
    :type comment_id: str
    :param text: e.g. 'Edited comment'
    :type text: str
    :param attachments: e.g. ['57', '58'], defaults to None
    :type attachments: Optional[List[str]], optional
    :return: response data
    :rtype: CommentResponse
    """
    url = f"{ENDPOINT}/{issue_id}/comments/{comment_id}"
    response = await client.patch(
        url, data
    )
    response_data = await response.json()
    response.close()
    return CommentEditResponse.parse_obj(response_data)


async def delete(client: BaseClient, issue_id: str, comment_id: str):
    """
    delete comment

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param comment_id: 689
    :type comment_id: str
    """
    url = f"{ENDPOINT}/{issue_id}/comments/{comment_id}"
    response = await client.delete(url)
    response.close()
