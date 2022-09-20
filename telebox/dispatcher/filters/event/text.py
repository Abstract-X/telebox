from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class TextFilter(AbstractEventFilter):

    def __init__(self, text: str, *, ignore_case: bool = False):
        self._text = text.lower() if ignore_case else text
        self._ignore_case = ignore_case

    def check_event(self, event: Message) -> bool:
        text = event.text

        if self._ignore_case:
            text = event.text.lower()

        return self._text == text
