from abc import ABC, abstractmethod

from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.dispatcher.router import Router


class AbstractReplyButton(ABC):
    @abstractmethod
    def get(self) -> KeyboardButton:
        pass

    def set_handler(self, router: Router) -> None:
        pass
