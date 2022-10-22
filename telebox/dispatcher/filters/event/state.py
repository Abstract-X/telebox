from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.typing import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.media_group import MediaGroup
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.state_machine.state import State
from telebox.state_machine.machine import StateMachine


class StateFilter(AbstractEventFilter):

    def __init__(self, *states: State, state_machine: StateMachine):
        self._states = set(states)
        self._state_machine = state_machine

    def get_value(self, event: Event, event_type: EventType) -> Optional[State]:
        if isinstance(event, (Message, CallbackQuery, MediaGroup)) and (event.chat_id is not None):
            return self._state_machine.get_state(chat_id=event.chat_id, user_id=event.user_id)

    def check_value(self, value: Optional[State]) -> bool:
        return value in self._states if self._states else value is not None
