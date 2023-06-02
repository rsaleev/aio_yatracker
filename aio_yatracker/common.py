import typing
from datetime import date, datetime
from enum import StrEnum

from pydantic import validator

from .base import TrackerModel
from .utils import convert_iso_8601_to_datetime


class ChangeType(StrEnum):
    ISSUE_UPDATED = "IssueUpdated"
    ISSUE_CREATED = "IssueCreated"
    ISSUE_MOVED = "IssueMoved"
    ISSUE_CLONED = "IssueCloned"
    ISSUE_COMMENT_ADDED = "IssueCommentAdded"
    ISSUE_COMMENT_UPDATED = "IssueCommentUpdated"
    ISSUE_COMMENT_REMOVED = "IssueCommentRemoved"
    ISSUE_WORKLOG_ADDED = "IssueWorklogAdded"
    ISSUE_WORKLOG_UPDATED = "IssueWorklogUpdated"
    ISSUE_WORKLOG_REMOVED = "IssueWorklogRemoved"
    ISSUE_COMMENT_REACTION_ADDED = "IssueCommentReactionAdded"
    ISSUE_COMMENT_REACTION_REMOVED = "IssueCommentReactionRemoved"
    ISSUE_VOTE_ADDED = "IssueVoteAdded"
    ISSUE_VOTE_REMOVED = "IssueVoteRemoved"
    ISSUE_LINKED = "IssueLinked"
    ISSUE_LINK_CHANGED = "IssueLinkChanged"
    ISSUE_UNLINKED = "IssueUnlinked"
    RELATED_ISSUE_RESOLUTION_CHANGED = "RelatedIssueResolutionChanged"
    ISSUE_ATTACHMENT_ADDED = "IssueAttachmentAdded"
    ISSUE_ATTACHMENT_REMOVED = "IssueAttachmentRemoved"
    ISSUE_WORKFLOW = "IssueWorkflow"


class Relationship(StrEnum):
    RELATES = "relates"
    DEPENDENT = "dependent"
    DEPENDS_ON = "depends"
    SUBTASK = "subtask"
    PARENT = "parent"
    DUPLICATES = "duplicates"
    DUPLICATED = "duplicated"
    EPIC = "epic"


class Attributes1(TrackerModel):
    id: str


class Attributes2(TrackerModel):
    id: str
    key: str


class Attributes3(TrackerModel):
    id: str
    display: str


class Attributes4(TrackerModel):
    self: str
    id: str
    display: str


class Attributes5(TrackerModel):
    self: str
    id: str
    key: str


class Attributes6(TrackerModel):
    self: str
    id: str
    key: str
    display: str


class Attributes7(TrackerModel):
    self: str
    id: str


class Attributes8(TrackerModel):
    key: str


class IssueModel(TrackerModel):
    self: str
    id: str
    key: str
    version: int
    last_comment_updated_at: typing.Optional[datetime]
    summary: str
    parent: typing.Optional[Attributes5]
    aliases: typing.Optional[typing.List[str]]
    description: typing.Optional[str]
    sprint: typing.Optional[typing.List[Attributes4]] = []
    type: Attributes6
    priority: Attributes6
    created_at: datetime
    followers: typing.Optional[typing.List[Attributes4]] = []
    created_by: Attributes4
    votes: typing.Optional[int]
    assignee: typing.Optional[typing.Optional[Attributes4]]
    queue: Attributes6
    updated_at: typing.Optional[datetime]
    status: Attributes6
    previous_status: typing.Optional[Attributes6]
    favorite: bool

    _validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )
    _validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )


class ChecklistItem(TrackerModel):
    id: str
    text: str
    text_html: str
    checked: bool
    checklist_item_type: str

class Checklist(TrackerModel):
    self: str
    id: str
    key: str
    version: int
    last_comment_updated_at: typing.Optional[datetime]
    pending_reply_from: typing.Optional[typing.List[Attributes4]]
    summary: str
    status_start_time: datetime
    updated_by: Attributes4
    description: typing.Optional[str]
    type: Attributes6
    priority: Attributes4
    previous_status_last_assignee: typing.Optional[Attributes4]
    created_at: datetime
    followers: typing.Optional[typing.List[Attributes4]]
    created_by: Attributes4
    checklist_items: typing.List[ChecklistItem]
    votes: int
    assignee: typing.Optional[Attributes4]
    deadline: typing.Optional[date]
    queue: Attributes6
    updated_at: datetime
    status: Attributes6
    previous_status: typing.Optional[Attributes6]
    favorite: bool

    _validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )
    _validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(
        convert_iso_8601_to_datetime
    )


class Project(TrackerModel):
    self: str
    id: str
    version: int
    key: str
    name: str
    description: typing.Optional[str]
    lead: Attributes4
    status: str
    start_date: typing.Optional[date]
    end_date: typing.Optional[date]
    queues: typing.Optional[typing.List[Attributes4]] = None


class ProjectStatus(StrEnum):
    DRAFT = "DRAFT"
    IN_PROGRESS = "IN PROGRESS"
    LAUNCHED = "LAUNCHED"
    POSTPONED = "POSTPONED"


class CommentType(StrEnum):
    STANDART = "STANDART"
    INCOMING = "INCOMING"
    OUTCOMING = "OUTCOMING"


class Transport(StrEnum):
    INTERNAL = "internal"
    EMAIL = "email"
