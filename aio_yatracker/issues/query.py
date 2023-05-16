from typing import Any, Dict, AsyncGenerator
from aio_yatracker.base import BaseClient, RequestParams

from .models import *


class Query:
    def __init__(self):
        self._endpoint = "issues"
        self._params = RequestParams()

    async def get_issues_parameters(
        self, client: BaseClient, issue_id: str
    ) -> IssueParametersResponse:
        """
        get_issues_parameters _summary_

        :param client: экземпляр клиента
        :type client: BaseClient
        :param issue_id: идентификатор задачи. Пример: QUEUE-10
        :type issue_id: str
        :raises ClientError, ClientConnectionError
        :return: ответ в случае успешной операции
        :rtype: IssueParametersResponse
        """
        url = f"{self._endpoint}/{issue_id}"
        response = await client.get(url, params=self._params.dict(by_alias=True))
        return IssueParametersResponse.parse_obj(await response.json())

    async def edit_issue(
        self, client: BaseClient, issue_id: str, data: IssueModificationRequest
    ) -> IssueModificationResponse:
        """
        edit_issue редактировать задачу

        :param client: экземпляр клиента
        :type client: BaseClient
        :param issue_id: идентификатор задачи. Пример: "QUEUE-10"
        :type issue_id: str
        :param data: тело запроса
        :type data: IssueModificationRequest
        :raises ClientError, ClientConnectionError
        :return: ответ в случае успешной операции
        :rtype: IssueModificationResponse
        """
        url = f"{self._endpoint}/{issue_id}"
        response = await client.patch(url=url, data=data)
        return IssueModificationResponse.parse_obj(await response.json())

    async def create_issue(
        self, client: BaseClient, data: IssueCreationRequest
    ) -> IssueCreationResponse:
        """
        create_issue создать задачу

        :param client: экземпляр клиента
        :type client: BaseClient
        :param data: тело запроса
        :type data: IssueModel
        :raises ClientError, ClientConnectionError
        :return: ответ в случае успешной операции
        :rtype: IssueCreationResponse
        """
        url = f"{self._endpoint}/"
        response = await client.post(url=url, data=data)
        return IssueCreationResponse.parse_obj(await response.json())

    async def move_issue(
        self,
        client: BaseClient,
        issue_id: str,
        dest_queue: str,
        data: IssueMoveRequest | None = None,
        notify: bool = True,
        notify_author: bool = False,
        move_all_fields: bool = False,
        initial_status: bool = False,
        expand: bool = False,
        expand_attachments: bool = False,
        expand_comments: bool = False,
        expand_workflow: bool = False,
        expand_transitions: bool = False,
    ) -> IssueMoveResponse:
        additional_params: Dict[str, Any] = {
            "queue": dest_queue,
            "notify": int(notify),
            "notify_author": int(notify_author),
            "move_all_field": int(move_all_fields),
            "initial_status": int(initial_status),
        }
        if expand:
            expand_arr = []
            if expand_attachments:
                expand_arr.append("attachmments")
            if expand_comments:
                expand_arr.append("comments")
            if expand_workflow:
                expand_arr.append("workflow")
            if expand_transitions:
                expand_arr.append("transitions")
            if expand_arr:
                additional_params["expand"] = ",".join(expand_arr)
        url = f"{self._endpoint}/{issue_id}/_move"
        response = await client.post(url=url, data=data, params=additional_params)
        return IssueMoveResponse.parse_obj(await response.json())

    votes: int

    async def count_issues(self, client: BaseClient, data: IssueCountRequest) -> int:
        """
        count_issues узнать количество задач

        :param client: экземпляр клиента
        :type client: BaseClient
        :param data: тело запроса
        :type data: IssueCountRequest
        :raises ClientError, ClientConnectionError
        :return: ответ в случае успешного выполнения
        :rtype: int
        """
        url = f"{self._endpoint}/_count"
        response = await client.post(url=url, data=data)
        return int(await response.text())

    async def search_issues(self, client: BaseClient, data: IssueSearchRequest)->AsyncGenerator:
        """
        search_issues поиск задач

        :param client: экземпляр клиента
        :type client: BaseClient
        :param data: тело запроса с фильтрами
        :type data: IssueSearchRequest
        :return: 
        :rtype: AsyncGenerator
        :yield: 
        :rtype: Iterator[AsyncGenerator]
        """
        url = f"{self._endpoint}/_search"
        response = await client.post(url=url, data=data)
        response.close()
        pagination = await client.handle_response(response)
        for i in range(1, pagination.total_pages + 1):
            pagination_params = self._params.copy()
            pagination_params.page = i
            paginated_response = await client.post(
                url=url, data=data, params=pagination_params.dict(by_alias=True)
            )
            paginated_response_model = [
                IssueSearchResponse.parse_obj(item)
                for item in await paginated_response.json()
            ]
            yield paginated_response_model


query = Query()
