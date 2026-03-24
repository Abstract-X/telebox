from typing import Any, Union

import orjson


def get_serialized_data(data: Any) -> bytes:
    return orjson.dumps(data)


def get_deserialized_data(data: Union[str, bytes]) -> Any:
    return orjson.loads(data)
