from typing import Union

import ujson

from telebox.utils.callback_data_builders.base import AbstractCallbackDataBuilder


FilterKey = Union[str, int]
Value = Union[str, int, float, bool, list, None]


class JSONCallbackDataBuilder(AbstractCallbackDataBuilder):

    def build(self, filter_key: FilterKey, value: Value = None) -> str:
        return ujson.dumps([filter_key, value])

    def parse(self, data: str) -> tuple[FilterKey, Value]:
        return tuple(ujson.loads(data))
