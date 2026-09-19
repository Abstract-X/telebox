from typing import Optional, Union

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.types.callback_query import CallbackQuery
from telebox.dispatcher.state_machine import StateMachine


class StateFilter(AbstractFilter):
    def __init__(self, *state_ids: int, machine: StateMachine, chat: bool = False):
        if not state_ids:
            raise ValueError("No state ids!")

        self._state_ids = frozenset(state_ids)
        self._machine = machine
        self._chat = chat

    def get_value(self, event: Union[Message, MediaGroup, CallbackQuery]) -> Optional[int]:
        chat_id = event.chat_id

        if chat_id is None:
            return

        if self._chat:
            user_id = None
        else:
            user_id = event.user_id

            if user_id is None:
                return

        history = self._machine.get_current_state_history(chat_id=chat_id, user_id=user_id)

        return history.state_id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._state_ids
