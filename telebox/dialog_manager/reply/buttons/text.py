from abc import ABC, abstractmethod

from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.bot.types.message import Message
from telebox.dialog_manager.reply.button import AbstractReplyButton


class AbstractTextButton(AbstractReplyButton, ABC):
    @staticmethod
    @abstractmethod
    def process_event(event: Message, deps) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_text(cls) -> str:
        pass

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.get_text())
