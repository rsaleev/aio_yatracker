import typing
from datetime import datetime

from pydantic import Field, root_validator

from ..base import TrackerModel
from ..common import *


class IssueParametersResponse(IssueModel):
    pass


class IssueModificationRequest(TrackerModel):
    summary: typing.Optional[str] = None
    parent: typing.Optional[Attributes8] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[
        typing.Union[Attributes8, typing.List[Attributes1], str]
    ] = None
    type: typing.Optional[Attributes2] = None
    priority: typing.Optional[Attributes2] = None
    followers: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    @root_validator(pre=True)
    def validate_non_empty(cls, values):
        if all([v is None for v in values]):
            raise ValueError("Empty request body")
        return values


class IssueModificationResponse(IssueModel):
    pass


class IssueCreationRequest(TrackerModel):
    summary: str
    queue: Attributes6 | str
    parent: typing.Optional[typing.Union[Attributes5, str]] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[typing.Union[typing.List[str], Attributes4]] = None
    type: typing.Optional[typing.Union[Attributes6, int, str]] = None
    priority: typing.Optional[typing.Union[Attributes6, int, str]] = None
    followers: typing.Optional[typing.Union[str, Attributes4]] = None
    assignee: typing.Optional[typing.Union[str, typing.List[str]]] = None
    attachment_ids: typing.Optional[typing.List[int]] = None


class IssueCreationResponse(IssueModel):
    pass


class IssueMoveRequest(IssueModel):
    summary: typing.Optional[str] = None
    parent: typing.Optional[Attributes5] = None
    description: typing.Optional[str] = None
    sprint: typing.Optional[Attributes4] = None
    type: typing.Optional[Attributes6] = None
    priority: typing.Optional[Attributes6] = None
    followers: typing.Optional[Attributes4] = None

    @root_validator(pre=True)
    def validate_non_empty(cls, values):
        if all([v is None for v in values]):
            raise ValueError("Empty request body")


class IssueMoveResponse(IssueModel):
    previous_queue: Attributes6
    previous_status: typing.Optional[Attributes6]


class IssueCountRequest(TrackerModel):
    filter: typing.Dict[str, typing.Any]
    query: typing.Optional[str] = None


class IssueSearchRequest(TrackerModel):
    filter: typing.Dict[str, typing.Any]
    query: typing.Optional[str] = None
    expand: typing.Optional[str] = None


class IssueSearchResponse(IssueModel):
    pass


class IssuePrioritiesResponse(TrackerModel):
    self: str
    id: int
    key: str
    version: int
    name: str
    order: int


class IssueTransitionResponse(Attributes4):
    to: Attributes6


class IssueTransitionOperationResponse(Attributes7):
    to: Attributes6
    screen: Attributes7


class IssueChangelogField(TrackerModel):
    field: Attributes4 | None
    from_state: typing.Optional[
        typing.Union[
            str,
            Attributes6,
            typing.List[Attributes6],
            Attributes4,
            typing.List[Attributes4],
            typing.List[str],
            typing.List[typing.Dict[str, typing.Any]],
        ]
    ] = Field(default=None, alias="from")
    to_state: typing.Optional[
        typing.Union[
            str,
            Attributes6,
            typing.List[Attributes6],
            Attributes4,
            typing.List[Attributes4],
            typing.List[str],
            typing.List[typing.Dict[str, typing.Any]],
        ]
    ] = Field(default=None, alias="to")


class IssueChangelogComments(TrackerModel):
    added: typing.Optional[typing.List[Attributes4]]
    deleted: typing.Optional[typing.List[Attributes4]]


class IssueChangeTriggers(TrackerModel):
    trigger: Attributes4
    success: bool
    message: str


class IssueChangelogResponse(TrackerModel):
    id: str
    self: str
    issue: Attributes6
    updated_at: datetime
    updated_by: Attributes4
    type: typing.Union[
        typing.Literal[ChangeType.ISSUE_ATTACHMENT_ADDED],
        typing.Literal[ChangeType.ISSUE_ATTACHMENT_REMOVED],
        typing.Literal[ChangeType.ISSUE_CLONED],
        typing.Literal[ChangeType.ISSUE_COMMENT_ADDED],
        typing.Literal[ChangeType.ISSUE_COMMENT_REACTION_ADDED],
        typing.Literal[ChangeType.ISSUE_COMMENT_REMOVED],
        typing.Literal[ChangeType.ISSUE_COMMENT_UPDATED],
        typing.Literal[ChangeType.ISSUE_CREATED],
        typing.Literal[ChangeType.ISSUE_LINK_CHANGED],
        typing.Literal[ChangeType.ISSUE_LINKED],
        typing.Literal[ChangeType.ISSUE_MOVED],
        typing.Literal[ChangeType.ISSUE_UNLINKED],
        typing.Literal[ChangeType.ISSUE_UPDATED],
        typing.Literal[ChangeType.ISSUE_VOTE_ADDED],
        typing.Literal[ChangeType.ISSUE_VOTE_REMOVED],
        typing.Literal[ChangeType.ISSUE_WORKFLOW],
        typing.Literal[ChangeType.ISSUE_WORKLOG_ADDED],
        typing.Literal[ChangeType.ISSUE_WORKLOG_REMOVED],
        typing.Literal[ChangeType.ISSUE_WORKLOG_UPDATED],
        typing.Literal[ChangeType.RELATED_ISSUE_RESOLUTION_CHANGED],
    ]
    transport: str
    fields: typing.Optional[typing.List[IssueChangelogField]]
    comments: typing.Optional[IssueChangelogComments]
    executed_triggers: typing.Optional[typing.List[IssueChangeTriggers]]


class IssueRelationshipCreateRequest(TrackerModel):
    relationship: typing.Union[
        typing.Literal[Relationship.DEPENDS_ON],
        typing.Literal[Relationship.DUPLICATES],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.DEPENDENT],
        typing.Literal[Relationship.DUPLICATED],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.PARENT],
        typing.Literal[Relationship.SUBTASK],
        typing.Literal[Relationship.RELATES],
    ]
    issue: str


class RelationshipType(TrackerModel):
    self: str
    id: typing.Union[
        typing.Literal[Relationship.DEPENDS_ON],
        typing.Literal[Relationship.DUPLICATES],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.DEPENDENT],
        typing.Literal[Relationship.DUPLICATED],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.PARENT],
        typing.Literal[Relationship.SUBTASK],
        typing.Literal[Relationship.RELATES],
    ]
    inward: str
    outward: str


class IssueRelationshipCreateResponse(TrackerModel):
    self: str
    id: str
    type: RelationshipType
    direction: str
    object: Attributes6
    created_by: Attributes4
    updated_by: Attributes4
    created_at: datetime
    updated_at: datetime


class IssueRelationshipResponse(TrackerModel):
    self: str
    id: str
    type: RelationshipType
    direction: str
    object: Attributes6
    created_by: Attributes4
    updated_by: Attributes4
    created_at: datetime
    updated_at: datetime
    assignee: typing.Optional[Attributes4]
    status: Attributes6


__all__ = [
    "IssueModel",
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
    "IssuePrioritiesResponse",
    "IssueTransitionResponse",
    "IssueTransitionOperationResponse",
    "IssueChangelogResponse",
    "IssueRelationshipCreateRequest",
    "IssueRelationshipCreateResponse",
    "IssueRelationshipResponse",
]
