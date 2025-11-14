from abc import ABC, abstractmethod
from typing import Union, Optional

from telebox.dialog_manager.keyboard import AbstractKeyboard
from telebox.bot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.message_entity import MessageEntity
from telebox.dispatcher.router import Router
from telebox.utils.unset import Unset, UNSET


class AbstractMenu(ABC):
    @abstractmethod
    def get_text(self, deps) -> str:
        pass

    @abstractmethod
    def get_keyboard(self, deps) -> AbstractKeyboard:
        pass

    @abstractmethod
    def set_handlers(self, router: Router) -> None:
        pass

    def get_media(self, deps) -> Optional[InputMedia]:
        return None

    def get_parse_mode(self) -> Union[str, None, Unset]:
        return UNSET

    def get_entities(self) -> Union[list[MessageEntity], None, Unset]:
        return UNSET

    def get_markup(self, deps) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        return self.get_keyboard(deps=deps).get()
