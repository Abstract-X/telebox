from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message


class TextFilter(AbstractEventFilter):

    def __init__(self, *texts: str, ignore_case: bool = False):
        self._texts = {i.lower() for i in texts} if ignore_case else set(texts)
        self._ignore_case = ignore_case

    def check(self, event: Message) -> bool:
        text = event.text

        if self._ignore_case:
            text = event.text.lower()

        return text in self._texts
