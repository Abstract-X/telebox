from typing import Union

import pytest

from telebox import get_callback_data
from telebox.callback_data import (
    get_parsed_callback_data,
    DATA_DELIMITER as DD,
    LIST_DELIMITER as LD
)


@pytest.mark.parametrize(
    ["id_", "payload"],
    [
        # Types
        [1, None],
        [2, "foo"],
        [3, 12345],
        [4, 12.345],
        [5, True],
        [6, False],
        [7, []],
        [8, [None]],
        [9, ["foo", "bar"]],
        [10, [123, 456]],
        [11, [12.34, 56.789]],
        [12, [None, "foo", 12345, 12.345, True, False]],

        # Escaping
        [13, f"{DD}foo{DD}{DD}bar{DD}"],
        [14, [f"{LD}foo{LD}{LD}", f"{LD}bar{LD}"]],
        [15, DD],
        [16, f"{DD}{DD}"],
        [17, [LD]],
        [18, [LD, LD]],
        [19, "\\"],
        [20, ["\\", "\\"]],
        [21, f"{DD}\\{LD}"],
        [22, [f"{DD}\\{LD}", f"\\{DD}\\{LD}\\"]],
        [23, "\\\\"]
    ]
)
def test(id_: int, payload: Union[str, int, float, bool, list, None]):
    data = get_callback_data(
        id_=id_,
        payload=payload
    )
    parsed_id, parsed_payload = get_parsed_callback_data(data)

    assert id_ == parsed_id
    assert payload == parsed_payload


@pytest.mark.parametrize(
    ["id_", "payload"],
    [
        [11111111111111111111111111111111111111111111111111111111111111111, None],
        [1, "foobarfoobarfoobarfoobarfoobarfoobarfoobarfoobarfoobarfoobarfo"]
    ]
)
def test_large_data(id_: int, payload: Union[str, int, float, bool, list, None]):
    with pytest.raises(ValueError):
        get_callback_data(id_=id_, payload=payload)


@pytest.mark.parametrize(
    ["id_", "payload"],
    [
        [1, [[]]],
        [2, ["foo", []]],
        [3, ["foo", ["bar"]]]
    ]
)
def test_nested_list(id_: int, payload: Union[str, int, float, bool, list, None]):
    with pytest.raises(ValueError):
        get_callback_data(id_=id_, payload=payload)
