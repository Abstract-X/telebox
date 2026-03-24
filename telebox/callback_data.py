from typing import Union, Optional


DATA_DELIMITER = "\x1E"
LIST_DELIMITER = "\x1F"
NEGATIVE_FLAG = "\x1D"
ENCODING_ALPHABET = r"""!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[~]^_`abcdefghijklmnopqrstuvwxyz{"""
DECODING_MAPPING = {
    character: i
    for i, character in enumerate(ENCODING_ALPHABET)
}
BASE = len(ENCODING_ALPHABET)
ESCAPING_CHARACTERS = ("\\", DATA_DELIMITER, LIST_DELIMITER)


def get_callback_data(
    callback_id: int,
    *,
    flow_id: Optional[int] = None,
    payload: Union[str, int, float, bool, list, None] = None
) -> str:
    parts = [_get_encoded_number(callback_id)]

    if flow_id is not None:
        parts.append(f"F{_get_encoded_number(flow_id)}")

    if payload is not None:
        parts.append(
            _get_serialized_object(payload)
        )

    return DATA_DELIMITER.join(parts)


def get_parsed_callback_data(
    data: str
) -> tuple[int, Optional[int], Union[str, int, float, bool, list, None]]:
    values = _get_parts(DATA_DELIMITER, data)
    callback_id = int(_get_decoded_number(values[0]))
    flow_id = None
    payload = None

    if len(values) == 1:
        pass
    elif len(values) == 2:
        if values[1].startswith("F"):
            flow_id = int(_get_decoded_number(values[1][1:]))
        else:
            payload = _get_deserialized_object(values[1])
    elif len(values) == 3:
        flow_id = int(_get_decoded_number(values[1][1:]))
        payload = _get_deserialized_object(values[2])
    else:
        raise ValueError(f"Parsing error {data!r}!")

    return callback_id, flow_id, payload


def _get_serialized_object(object_: Union[str, int, float, bool, list, None]) -> str:
    if isinstance(object_, str):
        escaped_string = _get_escaped_string(object_)

        return f"s{escaped_string}"
    elif isinstance(object_, bool):
        return "+" if object_ else "-"
    elif isinstance(object_, int):
        return f"i{_get_encoded_number(object_)}"
    elif object_ is None:
        return "n"
    elif isinstance(object_, float):
        return f"f{object_}"
    elif isinstance(object_, list):
        serialized_objects = []

        for i in object_:
            if isinstance(i, list):
                raise ValueError("Nested lists are not supported!")

            serialized_objects.append(
                _get_serialized_object(i)
            )

        escaped_string = LIST_DELIMITER.join(serialized_objects)

        return f"l{escaped_string}"
    else:
        raise TypeError(f"Unsupported type: {type(object_)}!")


def _get_deserialized_object(string: str):
    if string == "+":
        return True
    elif string == "-":
        return False
    elif string == "n":
        return None

    character = string[0]
    value = string[1:]

    if character == "l":
        if not value:
            return []

        return [
            _get_deserialized_object(i)
            for i in _get_parts(LIST_DELIMITER, value)
        ]
    elif character == "s":
        return _get_unescaped_string(value)
    elif character == "i":
        return int(_get_decoded_number(value))
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
    characters = []

    for i in string:
        if i in ESCAPING_CHARACTERS:
            characters.append("\\")

        characters.append(i)

    return "".join(characters)


def _get_unescaped_string(string: str) -> str:
    characters = []
    iterator = iter(string)

    for i in iterator:
        if i == "\\":
            next_character = next(iterator)

            if next_character in ESCAPING_CHARACTERS:
                characters.append(next_character)
        else:
            characters.append(i)

    return "".join(characters)


def _get_encoded_number(number: int) -> str:
    if number == 0:
        return ENCODING_ALPHABET[0]

    is_negative = number < 0
    number = abs(number)
    encoded_number = ""

    while number > 0:
        number, remainder = divmod(number, BASE)
        encoded_number = ENCODING_ALPHABET[remainder] + encoded_number

    if is_negative:
        encoded_number = NEGATIVE_FLAG + encoded_number

    return encoded_number


def _get_decoded_number(number: str) -> int:
    is_negative = number.startswith(NEGATIVE_FLAG)

    if is_negative:
        number = number[1:]

    decoded_number = 0

    for i in number:
        decoded_number = decoded_number * BASE + DECODING_MAPPING[i]

    return -decoded_number if is_negative else decoded_number
