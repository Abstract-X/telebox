from telebox.bot.types.inline_keyboard_button import InlineKeyboardButton
from telebox.bot.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChat
from telebox.dialog_manager.inline.button import AbstractInlineButton


class ChosenChatQueryButton(AbstractInlineButton):
    def __init__(
        self,
        text: str,
        query: SwitchInlineQueryChosenChat
    ):
        self.text = text
        self.query = query

    def get(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=self.text,
            switch_inline_query_chosen_chat=self.query
        )
