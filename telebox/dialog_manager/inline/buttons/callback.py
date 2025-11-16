from abc import ABC, abstractmethod
from typing import Union

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.callback_query import CallbackQuery
from telebox.dialog_manager.inline.button import AbstractInlineButton
from telebox.utils.callback_data import get_callback_data


class AbstractCallbackButton(AbstractInlineButton, ABC):
    def __init__(
        self,
        text: str,
        payload: Union[str, int, float, bool, list, None] = None
    ):
        self.text = text
        self.payload = payload

    @staticmethod
    @abstractmethod
    def process_event(event: CallbackQuery, deps) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_id(cls) -> int:
        pass

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            callback_data=get_callback_data(
                id_=self.get_id(),
                payload=self.payload
            )
        )
