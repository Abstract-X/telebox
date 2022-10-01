from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class TextFilter(AbstractEventFilter):

    def __init__(self, *texts: str, ignore_case: bool = False):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._ignore_case = ignore_case

    def get_value(self, event: Message) -> str:
        text = event.text

        if self._ignore_case:
            text = event.text.lower()

        return text

    def check_value(self, value: str) -> bool:
        return value in self._texts
