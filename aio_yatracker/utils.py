from datetime import datetime

def to_camel_case(arg: str) -> str:
    string_split = arg.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


def to_snake_case(arg: str) -> str:
    return "".join(["_" + i.lower() if i.isupper() else i for i in arg]).lstrip("_")


def convert_datetime_to_iso_8601(arg: datetime) -> str:
    return arg.astimezone().isoformat(sep="T", timespec="milliseconds")


def convert_iso_8601_to_datetime(arg: str):
    return datetime.fromisoformat(arg)
