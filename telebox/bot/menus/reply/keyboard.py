from typing import Union, Optional

from telebox.bot.menus.reply.button import AbstractReplyButton
from telebox.bot.types import ReplyKeyboardMarkup
from telebox.utils.unset import Unset, UNSET


class ReplyKeyboard:
    def __init__(
        self,
        buttons: Optional[list[list[AbstractReplyButton]]] = None,
        is_persistent: Union[bool, None, Unset] = UNSET,
        resize: Union[bool, None, Unset] = UNSET,
        one_time: Union[bool, None, Unset] = UNSET,
        input_field_placeholder: Union[str, None, Unset] = UNSET,
        selective: Union[bool, None, Unset] = UNSET
    ):
        self.buttons = buttons or []
        self.is_persistent = is_persistent
        self.resize = resize
        self.one_time = one_time
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective

    @property
    def rows(self) -> int:
        return len(self.buttons)

    def get_markup(self) -> ReplyKeyboardMarkup:
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

    def add_row(self, *buttons: AbstractReplyButton, index: Optional[int] = None) -> None:
        if index is None:
            self.buttons.append(list(buttons))
        else:
            self.buttons.insert(index, list(buttons))

    def get_row_length(self, *, index: int = -1) -> int:
        return len(self.buttons[index])

    def add_in_row(self, button: AbstractReplyButton, *, index: int = -1) -> None:
        self.buttons[index].append(button)
