from abc import ABC, abstractmethod

from telebox.bot.types.keyboard_button import KeyboardButton


class AbstractReplyButton(ABC):
    @abstractmethod
    def get(self) -> KeyboardButton:
        pass
