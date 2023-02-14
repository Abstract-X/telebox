import time

from telebox.bot.types.types.message import Message
from telebox.dispatcher.enums.event_type import EventType


class MediaGroupContainer:

    def __init__(self, event: Message, event_type: EventType):
        self.events = [event]
        self.event_type = event_type
        self.time = time.monotonic()

    def add_event(self, event: Message) -> None:
        self.events.append(event)
        self.time = time.monotonic()
