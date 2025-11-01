from typing import Union

from telebox.utils.unset import Unset


def get_full_name(first_name: str, last_name: Union[str, None, Unset]) -> str:
    return f"{first_name} {last_name}" if last_name else first_name
