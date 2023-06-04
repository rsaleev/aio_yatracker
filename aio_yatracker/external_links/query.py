from typing import AsyncGenerator

from ..base import BaseClient, RequestParams
from .models import *


async def applications(client: BaseClient) -> AsyncGenerator:
    """
    list external applications

    :param client: client instance
    :type client: BaseClient
    :rtype: AsyncGenerator
    :yield: List[ApplicationLinkResponse]
    :rtype: Iterator[AsyncGenerator]
    """
    url = "applications"
    response = await client.get(url)
    response.close()
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i, per_page=50).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            ApplicationLinkResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def issues(client: BaseClient, issue_id: str) -> AsyncGenerator:
    """
    list external issues

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :rtype: AsyncGenerator
    :yield: List[IssueLinkResponse]
    :rtype: Iterator[AsyncGenerator]

    """
    url = f"issues/{issue_id}/remotelinks"
    response = await client.get(url)
    response.close()
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i, per_page=50).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            IssueLinkResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def add(client: BaseClient, issue_id: str, data:IssueLinkRequest)->IssueLinkResponse:
    """
    add link

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param data: request body
    :type data: IssueLinkRequest
    :return: response data
    :rtype: IssueLinkResponse
    """
    url=f"issues/{issue_id}/remotelinks"
    response = await client.post(url, data, params={"backlink":"true"})
    response_data = await response.json()
    response.close()
    return IssueLinkResponse.parse_obj(response_data)

async def remove(client: BaseClient, issue_id:str, external_link_id:int):
    """
    remove link

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param external_link_id: e.g. 51455195
    :type external_link_id: str
    """
    url=f"issues/{issue_id}/remotelinks/{external_link_id}"
    response = await client.delete(url)
    response.close()

