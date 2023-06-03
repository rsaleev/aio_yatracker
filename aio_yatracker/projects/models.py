import typing
from datetime import date

from ..base import TrackerModel
from ..common import Attributes4, Attributes6, Project, ProjectStatus


class ProjectCreateRequest(TrackerModel):
    name: str
    queues: str


class ProjectCreateResponse(Project):
    pass


class ProjectParamsResponse(Project):
    pass


class ProjectsResponse(Project):
    pass


class ProjectIssueTypeConfig(TrackerModel):
    issue_type: Attributes6
    workflow: Attributes4
    resolutions: typing.List[Attributes6]


class ProjectQueueResponse(TrackerModel):
    self: str
    id: int
    key: str
    version: int
    name: str
    description: typing.Optional[str]
    lead: Attributes4
    assign_auto: bool
    default_type: Attributes6
    default_priority: Attributes6
    issue_types: typing.Optional[typing.List[Attributes6]]
    allow_external_mailing: typing.Optional[bool]
    add_issue_key_in_email: typing.Optional[bool]
    deny_voting: bool
    deny_conductor_autolink: bool
    use_component_permissions_intersection: bool
    use_last_signature: bool
    projects: typing.Optional[typing.List[Attributes4]]
    components: typing.Optional[typing.List[str]]
    versions: typing.Optional[typing.List[int]]
    types: typing.Optional[typing.Optional[Attributes4]]
    team: typing.Optional[Attributes4]
    workflows: typing.Optional[typing.Dict[str, typing.List[Attributes4]]]
    fields: typing.Optional[typing.List[str]]
    notification_fields: typing.Optional[typing.List[str]]
    issue_types_config: typing.Optional[typing.List[ProjectIssueTypeConfig]]


class ProjectEditRequest(TrackerModel):
    queues: str
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    lead: typing.Optional[typing.Union[str, int]] = None
    status: typing.Optional[
        typing.Union[
            typing.Literal[ProjectStatus.DRAFT],
            typing.Literal[ProjectStatus.IN_PROGRESS],
            typing.Literal[ProjectStatus.LAUNCHED],
            typing.Literal[ProjectStatus.POSTPONED],
        ]
    ] = None
    start_date: typing.Optional[date] = None
    end_date: typing.Optional[date] = None


class ProjectEditResponse(Project):
    pass


__all__ = [
    "ProjectCreateRequest",
    "ProjectCreateResponse",
    "ProjectParamsResponse",
    "ProjectsResponse",
    "ProjectQueueResponse",
    "ProjectEditRequest",
    "ProjectEditResponse",
]
