from typing import Any, Union

import orjson


def get_serialized_data(data: Any) -> str:
    return orjson.dumps(data).decode("UTF-8")


def get_deserialized_data(data: Union[str, bytes]) -> Any:
    return orjson.loads(data)
