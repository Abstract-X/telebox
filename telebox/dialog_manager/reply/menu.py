from abc import ABC, abstractmethod
from typing import Union

from telebox.dialog_manager.menu import AbstractMenu
from telebox.dialog_manager.reply.keyboard import ReplyKeyboard
from telebox.dispatcher.router import Router
from telebox.utils.unset import Unset, UNSET


class AbstractReplyMenu(AbstractMenu, ABC):
    @abstractmethod
    def get_keyboard(self, deps) -> ReplyKeyboard:
        pass


class ReplyMenu(AbstractReplyMenu):
    def __init__(
        self,
        text: str,
        keyboard: ReplyKeyboard,
        parse_mode: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.keyboard = keyboard
        self.parse_mode = parse_mode

    def get_text(self, deps) -> str:
        return self.text

    def get_keyboard(self, deps) -> ReplyKeyboard:
        return self.keyboard

    def set_handlers(self, router: Router) -> None:
        self.keyboard.set_handlers(router=router)

    def get_parse_mode(self) -> Union[str, None, Unset]:
        return self.parse_mode
