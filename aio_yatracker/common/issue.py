from ..base import TrackerModel, convert_iso_8601_to_datetime
from pydantic import validator
from datetime import datetime

import typing



class IssueParent(TrackerModel):
    self:str
    id:str
    key:str
    

class IssueUpdatedBy(TrackerModel):
    self:str
    id:str
    display:str

class IssueSprint(TrackerModel):
    self:str
    id:str
    display:str

class IssueType(TrackerModel):
    self:str
    id:int
    key:str
    display:str

class IssuePriority(TrackerModel):
    self:str
    id:int
    key:str
    display:str

class IssueFollowers(TrackerModel):
    self:str
    id:str
    display:str

class IssueCreatedBy(TrackerModel):
    self:str
    id:str
    display:str

class IssueAsignee(TrackerModel):
    self:str
    id:str
    display:str

class IssueQueue(TrackerModel):
    self:str
    id:str
    key:str
    display:str

class IssueStatus(TrackerModel):
    self:str
    id:str
    key:str
    display:str

class IssuePreviousStatus(TrackerModel):
    self:str
    id:str
    key:str
    display:str


class IssueModel(TrackerModel):
    self:str
    id:str
    key:str
    version:int
    last_comment_updated_at:typing.Optional[datetime]
    summary:str
    parent:typing.Optional[IssueParent]
    aliases: typing.Optional[typing.List[str]]
    description:str
    sprint:typing.Optional[typing.List[IssueSprint]] = []
    type:IssueType
    priority:IssuePriority
    created_at:datetime
    followers:typing.Optional[typing.List[IssueFollowers]] = []
    created_by:IssueCreatedBy
    votes:int
    assignee:typing.Optional[typing.Optional[IssueAsignee]]
    queue:IssueQueue
    updated_at:typing.Optional[datetime]
    status:IssueStatus
    previous_status:typing.Optional[IssuePreviousStatus]
    favorite:bool


    _validate_created_at = validator("created_at", allow_reuse=True, pre=True)(convert_iso_8601_to_datetime)
    _validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(convert_iso_8601_to_datetime)