from typing import Union

import ujson

from telebox.utils.callback_data_builders.builder import AbstractCallbackDataBuilder


Key = Union[str, int]
Value = Union[str, int, float, bool, list, None]


class JSONCallbackDataBuilder(AbstractCallbackDataBuilder):

    def get_string(self, key: Key, value: Value = None) -> str:
        return ujson.dumps([key, value])

    def get_data(self, string: str) -> tuple[Key, Value]:
        return tuple(ujson.loads(string))
