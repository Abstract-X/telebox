from dataclasses import dataclass
from typing import Union

from telebox.utils.unset import Unset, UNSET


@dataclass
class DefaultParameterSet:
    parse_mode: Union[str, Unset] = UNSET,
    disable_link_preview: Union[bool, Unset] = UNSET,
    disable_notification: Union[bool, Unset] = UNSET,
    protect_content: Union[bool, Unset] = UNSET
