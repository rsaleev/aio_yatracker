import typing
from datetime import datetime

from ..common.issue import IssueModel
from ..base import TrackerModel


class IssueParametersResponse(TrackerModel):
    __root__ : typing.Union[typing.List[IssueModel], IssueModel]
