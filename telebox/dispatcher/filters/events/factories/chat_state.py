from typing import Optional, Union, Iterable

from telebox.dispatcher.filters.events.factory import AbstractEventFilterFactory
from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.filters.events.cache import AbstractEventFilterCache
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.state_machine.state import State
from telebox.state_machine.machine import StateMachine


class ChatStateFilterCache(AbstractEventFilterCache):

    def __init__(self, machine: StateMachine):
        self._machine = machine

    def create(self, event: Union[Message, MediaGroup, CallbackQuery]) -> Optional[State]:
        if event.chat_id is not None:
            return self._machine.get_state(chat_id=event.chat_id)


class ChatStateFilter(AbstractEventFilter):

    def __init__(self, states: Iterable[State], cache: ChatStateFilterCache):
        if not states:
            raise ValueError("No states!")

        self._states = set(states)
        self._cache = cache

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

    def check_event(self, event: Union[Message, MediaGroup, CallbackQuery]) -> bool:
        return self._cache.get(event) in self._states


class ChatStateFilterFactory(AbstractEventFilterFactory):

    def __init__(self, machine: StateMachine):
        self._cache = ChatStateFilterCache(machine)

    def get(self, *states: State) -> ChatStateFilter:
        return ChatStateFilter(states, self._cache)
