import typing
from datetime import datetime

from pydantic import root_validator, validator

from ..base import TrackerModel
from ..common import *
from ..utils import convert_iso_8601_to_datetime


class IssueParent(TrackerModel):
    self: str
    id: str
    key: str


class IssueUpdatedBy(TrackerModel):
    self: str
    id: str
    display: str


class IssueSprint(TrackerModel):
    self: str
    id: str
    display: str


class IssueType(TrackerModel):
    self: str
    id: int
    key: str
    display: str


class IssuePriority(TrackerModel):
    self: str
    id: int
    key: str
    display: str


class IssueFollowers(TrackerModel):
    self: str
    id: str
    display: str


class IssueCreatedBy(TrackerModel):
    self: str
    id: str
    display: str


class IssueUpdateBy(TrackerModel):
    self: str
    id: str
    display: str


class IssueAsignee(TrackerModel):
    self: str
    id: str
    display: str


class IssueQueue(TrackerModel):
    self: str
    id: str
    key: str
    display: str


class IssueStatus(TrackerModel):
    self: str
    id: str
    key: str
    display: str


class IssuePreviousStatus(TrackerModel):
    self: str
    id: str
    key: str
    display: str


class IssueModel(TrackerModel):
    self: str
    id: str
    key: str
    version: int
    last_comment_updated_at: typing.Optional[datetime]
    summary: str
    parent: typing.Optional[IssueParent]
    aliases: typing.Optional[typing.List[str]]
    description: typing.Optional[str]
    sprint: typing.Optional[typing.List[IssueSprint]] = []
    type: IssueType
    priority: IssuePriority
    created_at: datetime
    followers: typing.Optional[typing.List[IssueFollowers]] = []
    created_by: IssueCreatedBy
    votes: int
    assignee: typing.Optional[typing.Optional[IssueAsignee]]
    queue: IssueQueue
    updated_at: typing.Optional[datetime]
    status: IssueStatus
    previous_status: typing.Optional[IssuePreviousStatus]
    favorite: bool

    _validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )
    _validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )


class IssueParametersResponse(TrackerModel):
    __root__: typing.Union[typing.List[IssueModel], IssueModel]


class IssueModificationRequest(TrackerModel):
    summary: typing.Optional[str] = None
    parent: typing.Optional[IssueParent] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[IssueSprint] = None
    type: typing.Optional[IssueType] = None
    priority: typing.Optional[IssuePriority] = None
    followers: typing.Optional[IssueFollowers] = None

    @root_validator(pre=True)
    def validate_non_empty(cls, values):
        if all([v is None for v in values]):
            raise ValueError("Empty request body")
        return values


class IssueModificationResponse(IssueModel):
    pass


class IssueCreationRequest(TrackerModel):
    summary: str
    queue: Queue | str
    parent: typing.Optional[Parent] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[typing.Union[typing.List[str], Sprint]] = None
    type: typing.Optional[typing.Union[Type, int, str]] = None
    priority: typing.Optional[typing.Union[Priority, int, str]] = None
    followers: typing.Optional[typing.Union[str, Follower]] = None
    assignee: typing.Optional[typing.List[str]] = None
    # unique: str = str(uuid4())
    attachment_ids: typing.Optional[typing.List[str]] = None


class IssueCreationResponse(IssueModel):
    pass


class IssueMoveRequest(IssueModel):
    summary: typing.Optional[str] = None
    parent: typing.Optional[IssueParent] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[IssueSprint] = None
    type: typing.Optional[IssueType] = None
    priority: typing.Optional[IssuePriority] = None
    followers: typing.Optional[IssueFollowers] = None

    @root_validator(pre=True)
    def validate_non_empty(cls, values):
        if all([v is None for v in values]):
            raise ValueError("Empty request body")


class IssueMoveResponse(IssueModel):
    self: str
    id: str
    key: str
    version: int
    aliases: typing.Optional[typing.List[str]]
    previous_queue: IssueQueue
    description: typing.Optional[str]
    type: IssueType
    created_at: datetime
    updated_at: typing.Optional[datetime]
    last_comment_updated_at: typing.Optional[datetime]
    summary: str
    updated_by: IssueUpdatedBy
    priority: IssuePriority
    followers: typing.Optional[typing.List[IssueFollowers]] = []
    created_by: IssueCreatedBy
    assignee: typing.Optional[typing.Optional[IssueAsignee]]
    queue: IssueQueue
    status: IssueStatus
    previous_status: typing.Optional[IssuePreviousStatus]
    favorite: bool

    _validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )
    _validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )


class IssueCountRequest(TrackerModel):
    filter: typing.Dict[str, typing.Any]
    query: typing.Optional[str] = None


class IssueSearchRequest(TrackerModel):
    filter: typing.Dict[str, typing.Any]
    query: typing.Optional[str] = None
    expand: typing.Optional[str] = None


class IssueSearchResponse(IssueModel):
    pass

__all__ = [
    "IssueQueue",
    "IssueModel",
    "IssueParent",
    "IssueSprint",
    "IssueType",
    "IssuePriority",
    "IssueFollowers",
    "IssueParametersResponse",
    "IssueModificationRequest",
    "IssueModificationResponse",
    "IssueCreationRequest",
    "IssueCreationResponse",
    "IssueMoveRequest",
    "IssueMoveResponse",
    "IssueCountRequest",
    "IssueSearchRequest",
    "IssueSearchResponse",
]
