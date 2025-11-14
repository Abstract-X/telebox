from abc import ABC, abstractmethod
from typing import Union

from telebox.bot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from telebox.bot.types.inline_keyboard_markup import InlineKeyboardMarkup
from telebox.dispatcher.router import Router


class AbstractKeyboard(ABC):
    @abstractmethod
    def get(self) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        pass

    @abstractmethod
    def set_handlers(self, router: Router) -> None:
        pass
