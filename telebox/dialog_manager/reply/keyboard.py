from typing import Union

from telebox.dispatcher.router import Router
from telebox.dialog_manager.keyboard import AbstractKeyboard
from telebox.dialog_manager.reply.button import AbstractReplyButton
from telebox.bot.types import ReplyKeyboardMarkup
from telebox.utils.unset import Unset, UNSET


class ReplyKeyboard(AbstractKeyboard):
    def __init__(
        self,
        buttons: list[list[AbstractReplyButton]],
        is_persistent: Union[bool, None, Unset] = UNSET,
        resize: Union[bool, None, Unset] = UNSET,
        one_time: Union[bool, None, Unset] = UNSET,
        input_field_placeholder: Union[str, None, Unset] = UNSET,
        selective: Union[bool, None, Unset] = UNSET
    ):
        self.buttons = buttons
        self.is_persistent = is_persistent
        self.resize = resize
        self.one_time = one_time
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective

    def get(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            keyboard=[
                [button.get() for button in row]
                for row in self.buttons
            ],
            is_persistent=self.is_persistent,
            resize_keyboard=self.resize,
            one_time_keyboard=self.one_time,
            input_field_placeholder=self.input_field_placeholder,
            selective=self.selective
        )

    def set_handlers(self, router: Router) -> None:
        for row in self.buttons:
            for button in row:
                button.set_handler(router=router)
