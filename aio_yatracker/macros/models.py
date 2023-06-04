from typing import List

from ..base import TrackerModel
from ..common import Macros, MacrosFieldChanges



class MacrosRequest(TrackerModel):
    name:str 
    body:str 
    field_changes:List[MacrosFieldChanges]
class MacrosResponse(Macros):
    pass

class MacrosCreateRequest(MacrosRequest):
    pass

class MacrosCreateResponse(Macros):
    pass 

class MacrosEditRequest(MacrosRequest):
    pass

class MacrosEditResponse(Macros):
    pass

__all__ = ["MacrosResponse", "MacrosCreateRequest", "MacrosCreateResponse", "MacrosEditRequest", "MacrosEditResponse"]




