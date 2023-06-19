from typing import AsyncGenerator

from ..base import BaseClient, RequestParams
from .models import *

ENDPOINT = "queues"


async def list(client: BaseClient, queue_id: str) -> AsyncGenerator:
    """
    list macros

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :rtype: AsyncGenerator
    :yield: List[MacrosResponse]
    :rtype: Iterator[AsyncGenerator]
    """
    url = f"{ENDPOINT}/{queue_id}/macros"
    response = await client.get(url=url)
    response.close()
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i, per_page=50).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            MacrosResponse.parse_obj(item) for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def get(client: BaseClient, queue_id: str, macros_id: str) -> MacrosResponse:
    """
    get macros

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param macros_id: 3
    :type macros_id: str
    :return: response data
    :rtype: MacrosResponse
    """
    url = f"{ENDPOINT}/{queue_id}/macros/{macros_id}"
    response = await client.get(url)
    response_data = await response.json()
    response.close()
    return MacrosResponse.parse_obj(response_data)


async def create(
    client: BaseClient, queue_id: str, data: MacrosCreateRequest
) -> MacrosCreateResponse:
    """
    create macros

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. 'QUEUE-1'
    :type queue_id: str
    :param data: request body
    :type data: MacrosCreateRequest
    :return: response data
    :rtype: MacrosCreateResponse
    """
    url = f"{ENDPOINT}/{queue_id}/macros"
    response = await client.post(url, data)
    response_data = await response.json()
    response.close()
    return MacrosCreateResponse.parse_obj(response_data)


async def edit(
    client: BaseClient, queue_id: str, macros_id: int, data: MacrosEditRequest
) -> MacrosEditResponse:
    """
    edit macros

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param macros_id: e.g. 3
    :type macros_id: int
    :param data: request body
    :type data: MacrosEditRequest
    :return: request data
    :rtype: MacrosEditResponse
    """
    url = f"{ENDPOINT}/{queue_id}/macros/{macros_id}"
    response = await client.patch(url, data)
    response_data = await response.json()
    response.close()
    return MacrosEditResponse.parse_obj(response_data)


async def delete(client: BaseClient, queue_id: str, macros_id: int):
    """
    delete macros

    :param client: client instance
    :type client: BaseClient
    :param queue_id: e.g. QUEUE-1
    :type queue_id: str
    :param macros_id: e.g. 9
    :type macros_id: int
    """
    url = f"{ENDPOINT}/{queue_id}/macros/{macros_id}"
    response = await client.delete(url)
    response.close()
