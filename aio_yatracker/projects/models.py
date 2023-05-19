import typing
from datetime import datetime

from ..base import TrackerModel
from ..common import Attributes6, Project, ProjectStatus


class ProjectCreateRequest(TrackerModel):
    name: str
    queues: str


class ProjectCreateResponse(Project):
    pass


class ProjectParamsResponse(Project):
    pass


class ProjectsResponse(TrackerModel):
    __root__: typing.List[Project]


class ProjectQueue(TrackerModel):
    self: str
    id: int
    key: str
    version: int
    name: str
    description: str
    lead: Attributes6
    assign_auto: bool
    default_type: Attributes6
    default_priority: Attributes6
    allow_external_mailing: bool
    add_issue_key_in_email: bool
    deny_voting: bool
    deny_conductor_autolink: bool
    use_component_permissions_intersection: bool
    use_last_signature: bool


class ProjectQueuesResponse(TrackerModel):
    __root__: typing.List[ProjectQueue]


class ProjectEditRequest(TrackerModel):
    queue: str
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    lead: typing.Optional[typing.Union[str, int]]
    status: typing.Union[
        typing.Literal[ProjectStatus.DRAFT],
        typing.Literal[ProjectStatus.IN_PROGRESS],
        typing.Literal[ProjectStatus.LAUNCHED],
        typing.Literal[ProjectStatus.POSTPONED],
    ]
    start_date: datetime
    end_date: datetime


class ProjectEditResponse(Project):
    pass


__all__ = [
    "ProjectCreateRequest",
    "ProjectCreateResponse",
    "ProjectParamsResponse",
    "ProjectsResponse",
    "ProjectQueuesResponse",
    "ProjectEditRequest",
    "ProjectEditResponse",
]
