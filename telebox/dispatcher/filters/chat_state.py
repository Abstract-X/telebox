from typing import Optional, Union

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.types.callback_query import CallbackQuery
from telebox.dispatcher.state_machine import StateMachine


class ChatStateFilter(AbstractFilter):
    def __init__(self, *state_ids: str, machine: StateMachine):
        if not state_ids:
            raise ValueError("No states!")

        self._state_ids = set(state_ids)
        self._machine = machine

    def get_value(self, event: Union[Message, MediaGroup, CallbackQuery]) -> Optional[int]:
        if event.chat_id is not None:
            return self._machine.get_bundle(chat_id=event.chat_id).state_id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._state_ids
