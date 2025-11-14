from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.dispatcher.router import Router
from telebox.dispatcher.type_hints import Handler
from telebox.dispatcher.filters.filters.callback_id import CallbackIDFilter
from telebox.dialog_manager.inline.button import AbstractInlineButton
from telebox.utils.callback_data import get_callback_data


class CallbackButton(AbstractInlineButton):
    def __init__(
        self,
        handler: Handler,
        text: str,
        id_: int,
        payload: Union[str, int, float, bool, list, None] = None
    ):
        self.handler = handler
        self.text = text
        self.id = id_
        self.payload = payload

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            callback_data=get_callback_data(
                id_=self.id,
                payload=self.payload
            )
        )

    def set_handler(self, router: Router) -> None:
        router.add_callback_query_handler(
            self.handler,
            CallbackIDFilter(self.id)
        )
