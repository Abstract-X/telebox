from typing import Union, Optional

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.ui.inline.button import AbstractInlineButton
from telebox.callback_data import get_callback_data
from telebox.context_values import flow_id_context, FromContext, OPTIONAL_FROM_CONTEXT
from telebox.unset import Unset, UNSET


class CallbackButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        callback_id: int,
        *,
        flow_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT,
        payload: Union[str, int, float, bool, list, None] = None,
        icon_custom_emoji_id: Union[str, None, Unset] = UNSET,
        style: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.callback_id = callback_id
        self.flow_id = flow_id
        self.payload = payload
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            callback_data=get_callback_data(
                callback_id=self.callback_id,
                flow_id=_get_flow_id(self.flow_id),
                payload=self.payload
            ),
            icon_custom_emoji_id=self.icon_custom_emoji_id,
            style=self.style
        )


def _get_flow_id(flow_id: Union[int, None, FromContext]) -> Optional[int]:
    if isinstance(flow_id, FromContext):
        return flow_id_context.get(None)

    return flow_id
