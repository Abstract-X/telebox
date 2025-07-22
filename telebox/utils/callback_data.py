from typing import Union


DATA_DELIMITER = "|"
LIST_DELIMITER = ":"
ESCAPING_CHARACTERS = ("\\", DATA_DELIMITER, LIST_DELIMITER)


def get_callback_data(id_: int, payload: Union[str, int, float, bool, list, None] = None) -> str:
    if payload is not None:
        serialized_payload = _get_serialized_object(payload)

        return f"{id_}{DATA_DELIMITER}{serialized_payload}"

    return str(id_)


def get_parsed_callback_data(data: str) -> tuple[int, Union[str, int, float, bool, list, None]]:
    values = _get_parts(DATA_DELIMITER, data)

    if len(values) == 1:
        id_ = values[0]
        payload = None
    elif len(values) == 2:
        id_, payload = values
        payload = _get_deserialized_object(payload)
    else:
        raise ValueError("Parsing error!")

    return int(id_), payload


def _get_serialized_object(object_) -> str:
    if isinstance(object_, str):
        escaped_string = _get_escaped_string(object_)

        return f"s{escaped_string}"
    elif isinstance(object_, bool):
        return "b1" if object_ else "b0"
    elif isinstance(object_, int):
        return f"i{object_}"
    elif object_ is None:
        return "n"
    elif isinstance(object_, float):
        return f"f{object_}"
    elif isinstance(object_, list):
        escaped_string = LIST_DELIMITER.join(
            _get_serialized_object(i) for i in object_
        )

        return f"l{escaped_string}"
    else:
        raise TypeError(f"Unsupported type: {type(object_)}!")


def _get_deserialized_object(string: str):
    character = string[0]
    value = string[1:]

    if character == "l":
        return [
            _get_deserialized_object(i)
            for i in _get_parts(LIST_DELIMITER, value)
        ]
    elif character == "s":
        return _get_unescaped_string(value)
    elif character == "b":
        return value == "1"
    elif character == "i":
        return int(value)
    elif string == "n":
        return None
    elif character == "f":
        return float(value)
    else:
        raise ValueError(f"Unsupported type character: {character!r}!")


def _get_parts(character: str, string: str):
    index = last_index = 0
    slice_ranges = []

    while index < len(string):
        if string[index] == "\\":
            index += 1
        elif string[index] == character:
            slice_ranges.append((last_index, index))
            last_index = index + 1

        index += 1

    slice_ranges.append((last_index, len(string)))

    return [
        string[start_index:end_index]
        for start_index, end_index in slice_ranges
    ]


def _get_escaped_string(string: str) -> str:
    escaped_string = string

    for i in ESCAPING_CHARACTERS:
        escaped_string = escaped_string.replace(i, f"\\{i}")

    return escaped_string


def _get_unescaped_string(string: str) -> str:
    result = []
    index = 0

    while index < len(string):
        if string[index] == "\\":
            next_index = index + 1

            if string[next_index] in ESCAPING_CHARACTERS:
                result.append(string[next_index])
                index += 2
        else:
            result.append(string[index])
            index += 1

    return "".join(result)
