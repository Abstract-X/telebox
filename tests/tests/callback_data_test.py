from typing import Union, Optional

import pytest

from telebox import get_callback_data
from telebox.callback_data import (
    get_parsed_callback_data,
    DATA_DELIMITER as DD,
    LIST_DELIMITER as LD
)


@pytest.mark.parametrize(
    "callback_id",
    [1, 123, 0, -1, -123]
)
@pytest.mark.parametrize(
    "flow_id",
    [None, 1, 123, 0, -1, -123]
)
@pytest.mark.parametrize(
    "payload",
    [
        None,
        "",
        "foo",
        "FOO",
        12345,
        *range(0, 92),
        -12345,
        0.0,
        -0.0,
        1e-10,
        -1e-10,
        1e10,
        -1e10,
        123.45,
        -123.45,
        True,
        False,
        [],
        [None],
        ["foo"],
        [123],
        [-123],
        [True],
        [False],
        [1.23],
        [-1.23],
        ["", ""],
        ["foo", ""],
        ["", "bar"],
        ["foo", "bar"],
        [123, 456],
        [-123, -456],
        [-123, 456],
        [123, -456],
        [12.34, 56.789],
        [-12.34, 56.789],
        [12.34, -56.789],
        [-12.34, -56.789],
        [None, "foo", 12345, 12.345, True, False],
        [None, "foo", -12345, 12.345, False, True],
        [None, "foo", 12345, -12.345, True, False],
        [None, "foo", -12345, -12.345, False, True],
        f"{DD}foo{DD}{DD}bar{DD}",
        f"{LD}foo{LD}{LD}", f"{LD}bar{LD}",
        DD,
        LD,
        f"{DD}{DD}",
        f"{LD}{LD}",
        f"{LD}{DD}",
        f"{DD}{LD}",
        [DD],
        [LD],
        [DD, DD],
        [LD, LD],
        [LD, DD],
        [DD, LD],
        [f"{DD}", f"{LD}"],
        [f"{DD}{LD}", f"{LD}{DD}"],
        "\\",
        "foo\\",
        ["\\", "\\"],
        f"{DD}\\{LD}",
        [f"{DD}\\{LD}", f"\\{DD}\\{LD}\\"],
        "\\\\",
        "\\\\\\"
    ]
)
def test(callback_id, flow_id: Optional[int], payload: Union[str, int, float, bool, list, None]):
    data = get_callback_data(callback_id, flow_id=flow_id, payload=payload)

    assert get_parsed_callback_data(data) == (callback_id, flow_id, payload)


@pytest.mark.parametrize(
    ["callback_id", "payload"],
    [
        [1, [[]]],
        [2, ["foo", []]],
        [3, ["foo", ["bar"]]]
    ]
)
def test_nested_list(callback_id: int, payload: Union[str, int, float, bool, list, None]):
    with pytest.raises(ValueError):
        get_callback_data(callback_id, payload=payload)
