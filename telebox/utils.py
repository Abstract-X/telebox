from typing import Any, Union

import orjson


def get_serialized_data(data: Any) -> bytes:
    return orjson.dumps(data)


def get_deserialized_data(data: Union[str, bytes]) -> Any:
    return orjson.loads(data)


def get_text_with_surrogates(text: str) -> bytes:
    return text.encode("UTF-16-LE")


def get_text_without_surrogates(text: bytes) -> str:
    return text.decode("UTF-16-LE")
