from .base import TrackerModel


class Follower(TrackerModel):
    id: str


class Parent(TrackerModel):
    id: str
    key: str


class Priority(TrackerModel):
    id: str
    key: str


class Queue(TrackerModel):
    id: str
    key: str


class Sprint(TrackerModel):
    id:str

class Type(TrackerModel):
    id:str
    key:str