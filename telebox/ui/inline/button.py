from abc import ABC, abstractmethod

from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton


class AbstractInlineButton(ABC):
    @abstractmethod
    def get(self) -> InlineKeyboardButton:
        pass
