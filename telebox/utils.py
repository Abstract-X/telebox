from dataclasses import dataclass
from typing import Union


class NotSetValue:
    pass


@dataclass
class RequestTimeout:
    connect_secs: Union[float, int]
    read_secs: Union[float, int]


NOT_SET_VALUE = NotSetValue()
