import time
from queue import Queue, SimpleQueue
from typing import Optional
from threading import Lock
from dataclasses import dataclass

from telebox.dispatcher.enums.event_type import EventType
from telebox.typing import Event as Event_


_DELAY_SECS = 0.05
_CHAT_ID_AND_USER_ID_GETTERS = {
    i: lambda event: (event.chat_id, event.user_id)
    for i in (
        EventType.MESSAGE,
        EventType.EDITED_MESSAGE,
        EventType.CALLBACK_QUERY,
        EventType.MY_CHAT_MEMBER,
        EventType.CHAT_MEMBER,
        EventType.CHAT_JOIN_REQUEST
    )
} | {
    i: lambda event: (None, event.user_id)
    for i in (
        EventType.INLINE_QUERY,
        EventType.CHOSEN_INLINE_RESULT,
        EventType.SHIPPING_QUERY,
        EventType.PRE_CHECKOUT_QUERY,
        EventType.POLL_ANSWER
    )
} | {
    i: lambda event: (event.chat_id, None)
    for i in (
        EventType.CHANNEL_POST,
        EventType.EDITED_CHANNEL_POST
    )
} | {
    i: lambda event: (None, None)
    for i in (
        EventType.POLL,
    )
}


@dataclass
class Event:
    event: Event_
    event_type: EventType
    chat_id: Optional[int] = None
    user_id: Optional[int] = None


class EventQueue:

    def __init__(self):
        self._events = Queue()
        self._chat_events: dict[int, SimpleQueue] = {}
        self._chat_event_lock = Lock()

    def add_event(
        self,
        event: Event_,
        event_type: EventType
    ) -> None:
        chat_id, user_id = _CHAT_ID_AND_USER_ID_GETTERS[event_type](event)
        event = Event(
            event=event,
            event_type=event_type,
            chat_id=chat_id,
            user_id=user_id
        )

        with self._chat_event_lock:
            if chat_id in self._chat_events:
                self._chat_events[chat_id].put(event, block=False)
            else:
                if chat_id is not None:
                    self._chat_events[chat_id] = SimpleQueue()

                self._events.put(event, block=False)

    def get_event(self) -> Event:
        return self._events.get()

    def set_event_as_processed(self, event: Event) -> None:
        try:
            with self._chat_event_lock:
                if event.chat_id in self._chat_events:
                    chat_events = self._chat_events[event.chat_id]

                    if not chat_events.empty():
                        next_event = chat_events.get(block=False)
                        self._events.put(next_event, block=False)

                    if chat_events.empty():
                        del self._chat_events[event.chat_id]
        finally:
            self._events.task_done()

    def wait_event_processing(self) -> None:
        while self._chat_events:
            time.sleep(_DELAY_SECS)

        self._events.join()
