from abc import ABC, abstractmethod
from typing import Union

from telebox.dispatcher.router import Router
from telebox.dialog_manager.menu import AbstractMenu
from telebox.dialog_manager.inline.keyboard import InlineKeyboard
from telebox.utils.unset import Unset, UNSET


class AbstractInlineMenu(AbstractMenu, ABC):
    @abstractmethod
    def get_keyboard(self, deps) -> InlineKeyboard:
        pass


class InlineMenu(AbstractInlineMenu):
    def __init__(
        self,
        text: str,
        keyboard: InlineKeyboard,
        parse_mode: Union[str, None, Unset] = UNSET
    ):
        self.text = text
        self.keyboard = keyboard
        self.parse_mode = parse_mode

    def get_text(self, deps) -> str:
        return self.text

    def get_keyboard(self, deps) -> InlineKeyboard:
        return self.keyboard

    def set_handlers(self, router: Router) -> None:
        self.keyboard.set_handlers(router=router)

    def get_parse_mode(self) -> Union[str, None, Unset]:
        return self.parse_mode
