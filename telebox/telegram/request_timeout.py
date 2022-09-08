from dataclasses import dataclass
from typing import Union


@dataclass
class RequestTimeout:
    connect_secs: Union[float, int]
    read_secs: Union[float, int]
