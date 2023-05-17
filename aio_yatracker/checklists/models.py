import typing
from datetime import datetime

from ..base import BaseClient, TrackerModel
from ..common import *


class ChecklistDeadline(TrackerModel):
    date: datetime
    deadline_type: str


class ChecklistCreateRequest(TrackerModel):
    text: str
    checked: typing.Optional[bool] = None
    assignee: typing.Optional[int] = None
    deadline: typing.Optional[ChecklistDeadline] = None


class ChecklistItem(TrackerModel):
    id: str
    text: str
    text_html: str
    checked: bool
    checklist_item_type: str


class ChecklistCreateResponse(Checklist):
    pass


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
    deadline_type: str = "date"
    is_exceeded: bool = False


class ChecklistParamsResponse(TrackerModel):
    id: str
    text: str
    text_html: str
    checked: bool
    assignee: typing.Optional[ChecklistParamsAssignee]
    deadline: typing.Optional[ChecklistDeadline]
    checklist_item_type: str


class ChecklistEditRequest(TrackerModel):
    text: str
    checked: typing.Optional[bool] = None
    assignee: typing.Optional[int] = None
    deadline: typing.Optional[ChecklistDeadline] = None


class ChecklistEditResponse(Checklist):
    pass


class ChecklistItemRemoveResponse(Checklist):
    pass

class ChecklistRemoveResponse(Checklist):
    pass




__all__ = [
    "ChecklistCreateRequest",
    "ChecklistCreateResponse",
    "ChecklistParamsResponse",
    "ChecklistEditRequest",
    "ChecklistEditResponse",
    "ChecklistItemRemoveResponse",
    "ChecklistRemoveResponse"
]
