import typing
from datetime import datetime

from ..base import TrackerModel
from ..common import Attributes4, Comment


class CommentCreateRequest(TrackerModel):
    text: str
    attachment_ids: typing.Optional[typing.List[str]] = None
    summonees: typing.Optional[typing.List[str]] = None
    maillist_summonees: typing.Optional[typing.List[str]] = None


class CommentCreateResponse(Comment):
    create_body: Attributes4
    update_body: Attributes4


class CommentListResponse(Comment):
    pass


class CommentEditRequest(TrackerModel):
    text: str
    attachment_ids: typing.Optional[typing.List[str]] = None
    summonees: typing.Optional[typing.List[str]] = None
    maillist_summonees: typing.Optional[typing.List[str]] = None


class CommentEditResponse(Comment):
    create_body: Attributes4
    update_body: Attributes4


__all__ = [
    "CommentCreateRequest",
    "CommentCreateResponse",
    "CommentListResponse",
    "CommentEditRequest",
    "CommentEditResponse",
]
