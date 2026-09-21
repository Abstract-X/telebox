from typing import Union

from telebox.ui.inline import CallbackButton
from telebox.unset import Unset, UNSET


class FlowCallbackButton(CallbackButton):
    def __init__(
        self,
        text: str,
        callback_id: int,
        flow_id: int,
        *,
        payload: Union[str, int, float, bool, list, None] = None,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        super().__init__(
            text=text,
            callback_id=callback_id,
            flow_id=flow_id,
            payload=payload,
            icon_custom_emoji_id=icon_custom_emoji_id,
            style=style
        )
