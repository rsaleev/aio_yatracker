from typing import AsyncGenerator, List

from ..base import BaseClient, RequestParams
from .models import *

ENDPOINT = "projects"


async def create(
    client: BaseClient, data: ProjectCreateRequest
) -> ProjectCreateResponse:
    """
    create project https://cloud.yandex.ru/docs/tracker/concepts/projects/create-project

    :param client: client instance
    :type client: BaseClient
    :param data: request body
    :type data: ProjectCreateRequest
    :return: response data
    :rtype: ProjectCreateResponse
    """
    url = f"{ENDPOINT}"
    response = await client.post(url=url, data=data)
    response_data = await response.json()
    response.close()
    return ProjectCreateResponse.parse_obj(response_data)


async def get(
    client: BaseClient, project_id: str, queues: bool = False
) -> ProjectParamsResponse:
    """
    get project https://cloud.yandex.ru/docs/tracker/concepts/projects/get-project

    :param client: client instance
    :type client: BaseClient
    :param project_id:
    :type project_id: str
    :return: response data
    :rtype: ProjectParamsResponse
    """
    additional_params = {}
    if queues:
        additional_params["expand"] = "queues"
    url = f"{ENDPOINT}/{project_id}"
    response = await client.get(url=url, params=additional_params)
    response_data = await response.json()
    response.close()
    return ProjectParamsResponse.parse_obj(response_data)


async def list(client: BaseClient, queues: bool = False) -> AsyncGenerator:
    """
    projects https://cloud.yandex.ru/docs/tracker/concepts/projects/get-projects

    :param client: client instance
    :type client: BaseClient
    :param queues: expand="queues", defaults to False
    :type queues: bool, optional
    :rtype: AsyncGenerator
    :yield: List[ProjectssResponse]
    :rtype: Iterator[AsyncGenerator]
    """
    additional_params = {}
    if queues:
        additional_params["expand"] = "queues"
    url = f"{ENDPOINT}"
    response = await client.get(url=url, params=additional_params)
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i).dict(by_alias=True)
        pagination_params.update(additional_params)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            ProjectsResponse.parse_obj(item) for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def queues(
    client: BaseClient,
    project_id: str,
    expand_all: bool = False,
    expand_projects: bool = False,
    expand_components: bool = False,
    expand_versions: bool = False,
    expand_types: bool = False,
    expand_team: bool = False,
    expand_workflows: bool = False,
    expand_fields: bool = False,
    expand_notification_fields: bool = False,
    expand_issue_types_config: bool = False,
    expand_enable_feature: bool = False,
    expand_signature_settings: bool = False,
) -> AsyncGenerator[List[ProjectQueueResponse], None]:
    """
    queues https://cloud.yandex.ru/docs/tracker/concepts/projects/get-project-queues

    :param client: _description_
    :type client: BaseClient
    :param project_id: e.g. 1
    :type project_id: str
    :param expand_all: add all fields, defaults to False
    :type expand_all: bool, optional
    :param expand_projects: add projects, defaults to False
    :type expand_projects: bool, optional
    :param expand_components: add components, defaults to False
    :type expand_components: bool, optional
    :param expand_versions: add versions, defaults to False
    :type expand_versions: bool, optional
    :param expand_types: add types, defaults to False
    :type expand_types: bool, optional
    :param expand_team: add team, defaults to False
    :type expand_team: bool, optional
    :param expand_workflows: add workflows, defaults to False
    :type expand_workflows: bool, optional
    :param expand_fields: add fields, defaults to False
    :type expand_fields: bool, optional
    :param expand_notification_fields: add notification_fields, defaults to False
    :type expand_notification_fields: bool, optional
    :param expand_issue_types_config: add issue_types, defaults to False
    :type expand_issue_types_config: bool, optional
    :param expand_enable_feature: add enable_featuer, defaults to False
    :type expand_enable_feature: bool, optional
    :param expand_signature_settings: add signature_settings, defaults to False
    :type expand_signature_settings: bool, optional
    :return generator
    :rtype: AsyncGenerator[ProjectQueuesResponse, None]
    :yield: ProjectsQueuesResponse
    :rtype: Iterator[AsyncIterator[AsyncGenerator[ProjectQueuesResponse, None]]]
    """
    url = f"{ENDPOINT}/{project_id}/queues"
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
    if expand_notification_fields:
        params["expand"] = "notification_fields"
    if expand_issue_types_config:
        params["expand"] = "issue_types_config"
    if expand_enable_feature:
        params["expand"] = "enable_feature"
    if expand_signature_settings:
        params["expand"] = "expand_signature_settings"
    response = await client.get(url=url, params=params)
    pagination = await client.handle_response(response)
    for i in range(1, pagination.total_pages + 1):
        pagination_params = RequestParams(page=i).dict(by_alias=True)
        pagination_params.update(params)
        paginated_response = await client.get(url=url, params=pagination_params)
        paginated_response_model = [
            ProjectQueueResponse.parse_obj(item)
            for item in await paginated_response.json()
        ]
        yield paginated_response_model
        paginated_response.close()


async def edit(
    client: BaseClient,
    project_id: str,
    version: int,
    data: ProjectEditRequest,
    queues: bool = False,
) -> ProjectEditResponse:
    """
    edit https://cloud.yandex.ru/docs/tracker/concepts/projects/update-project

    :param client: client instance
    :type client: BaseClient
    :param project_id: e.g. 1
    :type project_id: str
    :param version: _e.g. 1
    :type version: int
    :param data: _request body_
    :type data: ProjectEditRequest
    :return: _description_
    :rtype: ProjectEditResponse
    """
    url = f"{ENDPOINT}/{project_id}"
    params = {}
    params["version"] = version
    if queues:
        params["expand"] = "queues"
    response = await client.put(url=url, data=data, params=params)
    response_data = await response.json()
    response.close()
    return ProjectEditResponse.parse_obj(response_data)


async def delete(client: BaseClient, project_id: str) -> None:
    """
    delete https://cloud.yandex.ru/docs/tracker/concepts/projects/delete-project

    :param client: client instance
    :type client: BaseClient
    :param project_id: e.g. 1
    :type project_id: str
    """
    url = f"{ENDPOINT}/{project_id}"
    response = await client.delete(url=url)
    response.close()
