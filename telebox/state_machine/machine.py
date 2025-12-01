from typing import Optional, Union

from telebox.state_machine.storage import AbstractStateStorage
from telebox.state_machine.magazine import StateMagazine
from telebox.utils.context import Context, CONTEXT, OPTIONAL_CONTEXT, event_context, get_event_value
from telebox.dispatcher.type_hints import Event


class StateMachine:
    def __init__(self, initial_state: str, storage: AbstractStateStorage):
        self.initial_state = initial_state
        self._storage = storage

    def get_state(
        self,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT
    ) -> str:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.state

    def get_previous_state(
        self,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT
    ) -> Optional[str]:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.previous_state

    def get_states(
        self,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT
    ) -> list[str]:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.states

    def set_state(
        self,
        state: str,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT
    ) -> None:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)
        magazine.set_state(state)
        self._save_magazine(magazine, chat_id=chat_id, user_id=user_id)

    def _load_magazine(self, *, chat_id: int, user_id: Optional[int] = None) -> StateMagazine:
        states = self._storage.load_states(chat_id=chat_id, user_id=user_id)

        if not states:
            states = [self.initial_state]

        return StateMagazine(states)

    def _save_magazine(
        self,
        magazine: StateMagazine,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        self._storage.save_states(magazine.states, chat_id=chat_id, user_id=user_id)


def _get_chat_id_and_user_id(
    chat_id: Union[int, Context],
    user_id: Union[int, Context, None]
) -> tuple[int, Optional[int]]:
    if isinstance(chat_id, Context):
        chat_id = get_event_value("chat_id", optional=chat_id.optional)

    if isinstance(user_id, Context):
        user_id = get_event_value("user_id", optional=user_id.optional)

    return chat_id, user_id


def _get_event(event: Union[Event, Context, None]) -> Optional[Event]:
    if isinstance(event, Context):
        event = event_context.get()

    return event
