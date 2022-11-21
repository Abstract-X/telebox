from typing import Union

import ujson

from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder


Key = Union[str, int]
Value = Union[str, int, float, bool, list, None]


class JSONCallbackDataBuilder(AbstractCallbackDataBuilder):

    def get_builded_data(self, key: Key, value: Value = None) -> str:
        return ujson.dumps([key, value])

    def get_parsed_data(self, data: str) -> tuple[Key, Value]:
        return tuple(ujson.loads(data))
