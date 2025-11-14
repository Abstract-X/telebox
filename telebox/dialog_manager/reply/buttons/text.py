from telebox.bot.types.keyboard_button import KeyboardButton
from telebox.dispatcher.router import Router
from telebox.dispatcher.type_hints import Handler
from telebox.dispatcher.filters.filters.text import TextFilter
from telebox.dialog_manager.reply.button import AbstractReplyButton


class TextButton(AbstractReplyButton):
    def __init__(self, handler: Handler, text: str):
        self.handler = handler
        self.text = text

    def get(self) -> KeyboardButton:
        return KeyboardButton(text=self.text)

    def set_handler(self, router: Router) -> None:
        router.add_message_handler(
            self.handler,
            TextFilter(self.text)
        )
