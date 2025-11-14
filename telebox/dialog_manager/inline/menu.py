from abc import ABC, abstractmethod
from typing import Union, Optional

from telebox.dispatcher.router import Router
from telebox.dialog_manager.menu import AbstractMenu
from telebox.dialog_manager.inline.keyboard import InlineKeyboard
from telebox.bot.types.input_media import InputMedia
from telebox.bot.types.message_entity import MessageEntity
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
        parse_mode: Union[str, None, Unset] = UNSET,
        entities: Union[list[MessageEntity], None, Unset] = UNSET,
        media: Optional[InputMedia] = None
    ):
        self.text = text
        self.keyboard = keyboard
        self.parse_mode = parse_mode
        self.entities = entities
        self.media = media

    def get_text(self, deps) -> str:
        return self.text

    def get_keyboard(self, deps) -> InlineKeyboard:
        return self.keyboard

    def get_media(self, deps) -> Optional[InputMedia]:
        return self.media

    def set_handlers(self, router: Router) -> None:
        self.keyboard.set_handlers(router=router)

    def get_parse_mode(self) -> Union[str, None, Unset]:
        return self.parse_mode

    def get_entities(self) -> Union[list[MessageEntity], None, Unset]:
        return self.entities
