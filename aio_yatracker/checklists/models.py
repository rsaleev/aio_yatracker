import typing
from datetime import date, datetime

from ..base import TrackerModel
from ..common import (
    Attributes4,
    Attributes6,
    Checklist,
    convert_iso_8601_to_datetime,
    validator,
)


class ChecklistDeadline(TrackerModel):
    date: datetime
    deadline_type: str


class ChecklistCreateRequest(TrackerModel):
    text: str
    checked: typing.Optional[bool] = None
    assignee: typing.Optional[int] = None
    deadline: typing.Optional[ChecklistDeadline] = None


class ChecklistParamsAssignee(TrackerModel):
    id: str
    display: str
    passport_uid: int
    login: str
    first_name: str
    last_name: str
    email: str
    tracker_uid: int


class ChecklistParamsDeadline(TrackerModel):
    date: datetime
    deadline_type: str
    is_exceeded: bool


class ChecklistItem(TrackerModel):
    id: str
    text: str
    text_html: str
    checked: bool
    checklist_item_type: str
    assignee: typing.Optional[ChecklistParamsAssignee]
    deadline: typing.Optional[ChecklistDeadline]
    checklist_item_type: str


class ChecklistCreateResponse(Checklist):
    pass


class ChecklistParamsResponse(ChecklistItem):
    pass


class ChecklistEditRequest(TrackerModel):
    text: str
    checked: typing.Optional[bool] = None
    assignee: typing.Optional[int] = None
    deadline: typing.Optional[ChecklistDeadline] = None


class ChecklistEditResponse(Checklist):
    pass


class ChecklistItemRemoveResponse(Checklist):
    pass


class ChecklistRemoveResponse(TrackerModel):
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
    checklist_items: typing.Optional[typing.List[ChecklistItem]]
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


__all__ = [
    "ChecklistCreateRequest",
    "ChecklistCreateResponse",
    "ChecklistParamsResponse",
    "ChecklistEditRequest",
    "ChecklistEditResponse",
    "ChecklistItemRemoveResponse",
    "ChecklistRemoveResponse",
    "ChecklistDeadline",
    "ChecklistItem",
]
