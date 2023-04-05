from collections import deque
from typing import Optional
from threading import Lock, Condition
from dataclasses import dataclass

from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.typing import Event as Event_
from telebox.dispatcher.utils.events import get_event_chat_id, get_event_user_id


@dataclass
class Event:
    event: Event_
    event_type: EventType
    chat_id: Optional[int] = None
    user_id: Optional[int] = None


class EventQueue:

    def __init__(self):
        self._events = deque()
        self._chat_events: dict[int, deque] = {}
        self._unprocessed_events = 0
        self._lock = Lock()
        self._new_event_condition = Condition(self._lock)
        self._all_events_processed_condition = Condition(self._lock)

    def add_event(self, event: Event_, event_type: EventType) -> None:
        event = Event(
            event=event,
            event_type=event_type,
            chat_id=get_event_chat_id(event),
            user_id=get_event_user_id(event)
        )

        with self._new_event_condition:
            self._unprocessed_events += 1

            if event.chat_id in self._chat_events:
                self._chat_events[event.chat_id].append(event)
            else:
                if event.chat_id is not None:
                    self._chat_events[event.chat_id] = deque()

                self._events.append(event)
                self._new_event_condition.notify()

    def get_event(self) -> Event:
        with self._new_event_condition:
            while not self._events:
                self._new_event_condition.wait()

            return self._events.popleft()

    def set_event_completion(self, *, chat_id: Optional[int] = None) -> None:
        with self._all_events_processed_condition:
            if chat_id in self._chat_events:
                chat_events = self._chat_events[chat_id]

                if chat_events:
                    next_event = chat_events.popleft()
                    self._events.append(next_event)

                if not chat_events:
                    del self._chat_events[chat_id]

            self._unprocessed_events -= 1

            if not self._unprocessed_events:
                self._all_events_processed_condition.notify_all()

    def wait_events(self) -> None:
        with self._all_events_processed_condition:
            while self._unprocessed_events:
                self._all_events_processed_condition.wait()
