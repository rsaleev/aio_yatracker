import typing
from datetime import datetime

from ..base import TrackerModel
from ..common import Attributes4, Relationship


class Application(TrackerModel):
    self: str
    id: str
    type: str
    name: str


class ApplicationLinkResponse(Application):
    pass


class IssueLinkType(TrackerModel):
    self: str
    id: str
    inward: str
    outward: str


class IssueLinkObject(TrackerModel):
    self: str
    id: str
    key: str
    application: Application


class IssueLinkResponse(TrackerModel):
    self: str
    id: int
    type: IssueLinkType
    direction: str
    object: IssueLinkObject
    created_by: Attributes4
    updated_by: Attributes4
    created_at: datetime
    updated_at: datetime


class IssueLinkRequest(TrackerModel):
    relationship: typing.Union[
        typing.Literal[Relationship.DEPENDENT],
        typing.Literal[Relationship.DEPENDS_ON],
        typing.Literal[Relationship.DUPLICATED],
        typing.Literal[Relationship.DUPLICATES],
        typing.Literal[Relationship.EPIC],
        typing.Literal[Relationship.PARENT],
        typing.Literal[Relationship.RELATES],
        typing.Literal[Relationship.SUBTASK],
    ]
    key: str
    origin: str



__all__ = ["ApplicationLinkResponse", "IssueLinkRequest", "IssueLinkResponse"]
