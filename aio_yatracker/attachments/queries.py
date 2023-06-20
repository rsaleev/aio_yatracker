import os
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import AsyncGenerator

import aiofiles
from aiohttp import FormData

from ..base import BaseClient, RequestParams
from .models import Attachment

ENDPOINT = "issues"


async def list(client: BaseClient, issue_id: str) -> AsyncGenerator:
    """
    list attachments

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :return: generator
    :rtype: AsyncGenerator
    :yield: List[Attachment]
    :rtype: Iterator[AsyncGenerator]
    """
    url = f"{ENDPOINT}/{issue_id}/attachments"
    response = await client.get(url)
    response.close()
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i, per_page=50).dict(by_alias=True)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            Attachment.parse_obj(item) for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def file(
    client: BaseClient, issue_id: str, attachment_id: str, filename: str
) -> str:
    """
    download file

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param attachment_id: 459
    :type attachment_id: str
    :param filename: e.g. attachment.txt
    :type filename: str
    :return: file content
    :rtype: BytesIO
    """
    url = f"{issue_id}/attachments/{attachment_id}/{filename}"
    response = await client.get(url)
    prefix, suffix = filename.split(".")
    tf = NamedTemporaryFile(prefix=prefix, suffix=suffix, delete=False)
    async with aiofiles.open(tf.name, "wb") as f:
        await f.write(await response.read())
    return tf.name


async def thumbnail(client: BaseClient, issue_id: str, attachment_id: str) -> str:
    """
    download thumbnail

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param attachment_id: e.g.
    :type attachment_id: str
    :return: _description_
    :rtype: str
    """
    url = f"{issue_id}/thumbnails/{attachment_id}"
    response = await client.get(url)
    tf = NamedTemporaryFile(prefix=attachment_id, suffix="jpeg", delete=False)
    async with aiofiles.open(tf.name, "wb") as f:
        await f.write(await response.read())
    return tf.name


async def add(
    client: BaseClient, issue_id: str, data: str | BytesIO, filename: str = ""
) -> Attachment:
    """
    add attachment

    :param client:
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param data: full path or filedata
    :type data: str | BytesIO
    :param filename: e.g. attachment.txt, defaults to ""
    :type filename: str, optional
    :return: response data
    :rtype: Attachment
    """
    url = f"{issue_id}/attachments"
    fd = FormData()
    fd.add_field("file", data, filename=filename)
    headers = client._headers
    headers["Content-Type"] = "multipart/form-data"
    response = await client._session.post(
        f"/{client._version}/{url}", data=fd, headers=headers
    )
    respose_data = response.json()
    return Attachment.parse_obj(respose_data)


async def temp(
    client: BaseClient, data: str | BytesIO, filename: str = ""
) -> Attachment:
    """
    add temporary attachment

    :param client:
    :type client: BaseClient
    :param data: full path or filedata
    :type data: str | BytesIO
    :param filename: e.g. attachment.txt, defaults to ""
    :type filename: str, optional
    :return: response data
    :rtype: Attachment
    """
    url = f"attachments"
    fd = FormData()
    fd.add_field("file", data, filename=filename)
    headers = client._headers
    headers["Content-Type"] = "multipart/form-data"
    response = await client._session.post(
        f"/{client._version}/{url}", data=fd, headers=headers
    )
    respose_data = response.json()
    return Attachment.parse_obj(respose_data)


async def remove(client: BaseClient, issue_id: str, attachment_id: str):
    """
    remove attachment

    :param client: client instance
    :type client: BaseClient
    :param issue_id: e.g. QUEUE-1
    :type issue_id: str
    :param attachment_id: e.g. 459
    :type attachment_id: str
    """
    url = f"{issue_id}/attachments/{attachment_id}"
    await client.delete(url)
