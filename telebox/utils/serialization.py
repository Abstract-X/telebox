from typing import Any

import orjson


def get_serialized_data(data: Any) -> str:
    return orjson.dumps(data).decode("UTF-8")


def get_deserialized_data(data: str) -> Any:
    return orjson.loads(data)
