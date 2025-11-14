from abc import ABC, abstractmethod

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.dispatcher.router import Router


class AbstractInlineButton(ABC):
    @abstractmethod
    def get(self) -> InlineKeyboardButton:
        pass

    def set_handler(self, router: Router) -> None:
        pass
