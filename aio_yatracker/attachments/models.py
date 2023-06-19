from datetime import datetime

from ..base import TrackerModel
from ..common import Attributes4


class Metadata(TrackerModel):
    size:int


class Attachment(TrackerModel):
    self:str
    id:str 
    name:str
    content:str
    thumbnail:str
    created_by:Attributes4
    created_at: datetime
    mimetype:str
    size:int
    metadata:Metadata
