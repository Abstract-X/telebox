from typing import Optional, Union

from telebox.dispatcher.filters.factory import AbstractFilterFactory
from telebox.dispatcher.filters.filter import AbstractFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.types.callback_query import CallbackQuery
from telebox.state_machine.state import State
from telebox.state_machine.machine import StateMachine


class ChatStateFilter(AbstractFilter):

    def __init__(self, *states: State, machine: StateMachine):
        if not states:
            raise ValueError("No states!")

        self._states = set(states)
        self._machine = machine

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.CHANNEL_MEDIA_GROUP,
            EventType.CALLBACK_QUERY
        }

    def get_value(self, event: Union[Message, MediaGroup, CallbackQuery]) -> Optional[State]:
        if event.chat_id is not None:
            return self._machine.get_state(chat_id=event.chat_id)

    def check_value(self, value: Optional[State]) -> bool:
        return value in self._states


class ChatStateFilterFactory(AbstractFilterFactory):

    def __init__(self, machine: StateMachine):
        self._machine = machine

    def get(self, *states: State) -> ChatStateFilter:
        return ChatStateFilter(*states, machine=self._machine)
