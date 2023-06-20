from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import Field

from ..base import TrackerModel
from ..common import Attributes4, Attributes6, Queue, QueueIssueTypeConfig


class QueueRequest(TrackerModel):
    key: str
    name: str
    lead: str
    default_type: str = "task"
    default_priority: str = "normal"
    issues_types_config: QueueIssueTypeConfig


class QueueResponse(Queue):
    pass


class QueueVersionResponse(TrackerModel):
    self: str
    id: int
    version: int
    queue: Attributes4
    name: str
    description: str
    start_date: date
    due_date: Optional[date]
    released: bool
    archived: bool


class QueueFieldsSchema(TrackerModel):
    type: str
    required: bool


class QueueFieldsOptionsProvider(TrackerModel):
    type: str
    values: Dict[str, List[str]]
    defaults: List[str]


class QueueFieldsResponse(TrackerModel):
    self: str
    id: str
    name: str
    version: int
    schema_: QueueFieldsSchema = Field(alias="schema")
    readonly: bool
    options: bool
    suggest: bool
    options_provider: QueueFieldsOptionsProvider
    query_provider: Dict[str, str]
    order: int


class QueueTagsRequest(TrackerModel):
    tag: str


class QueueAutoActionRequest(TrackerModel):
    name: str
    filter: Dict[str, Any]
    actions: List[Dict[str, Any]]


class QueueAutoActionResponse(TrackerModel):
    id: int
    self: str
    queue: Attributes6
    name: str
    version: int
    active: bool
    created: datetime
    updated: datetime
    filter: Dict[str, Any]
    actions: List[Dict[str, Any]]
    enable_notifications: bool
    total_issues_processed: int
    interval_millis: int
    calendar: Dict[str, Any]


class QueueTriggerRequest(TrackerModel):
    name: str
    actions: List[Dict[str, Any]]
    conditions: Optional[List[Dict[str, Any]]]
    active: bool


class QueueTriggerAction(TrackerModel):
    type: str
    id: int
    status: Attributes6


class QueueTriggerResponse(TrackerModel):
    id: int
    self: str
    queue: Attributes6
    name: str
    order: str
    actions: List[QueueTriggerAction]
    conditions: List[Dict[str, Any]]
    version: int
    active: bool


__all__ = [
    "QueueRequest",
    "QueueResponse",
    "QueueVersionResponse",
    "QueueFieldsResponse",
    "QueueTagsRequest",
    "QueueAutoActionRequest",
    "QueueAutoActionResponse",
    "QueueTriggerRequest",
    "QueueTriggerResponse",
    "Attributes4",
    "Attributes6",
    "QueueIssueTypeConfig",
]
