from typing import Optional, Union, Callable

from telebox.state_machine.errors import PreviousStateNotFoundError
from telebox.state_machine.storage import AbstractStateStorage
from telebox.state_machine.magazine import StateMagazine
from telebox.context_values import FromContext, FROM_CONTEXT, OPTIONAL_FROM_CONTEXT, event_context, get_event_value
from telebox.dispatcher.type_hints import Event
from telebox.contexts import StateContext
from telebox.deps import DepsBase


class StateMachine:
    def __init__(self, initial_state: str, storage: AbstractStateStorage, deps: DepsBase):
        self.initial_state = initial_state
        self._storage = storage
        self._deps = deps
        self._enter_hooks: dict[str, list[Callable[[StateContext], None]]] = {}
        self._exit_hooks: dict[str, list[Callable[[StateContext], None]]] = {}

    def add_enter_hook(self, state: str, hook: Callable[[StateContext], None]) -> None:
        self._enter_hooks.setdefault(state, []).append(hook)

    def add_exit_hook(self, state: str, hook: Callable[[StateContext], None]) -> None:
        self._exit_hooks.setdefault(state, []).append(hook)

    def get_state(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ) -> str:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.state

    def get_previous_state(
        self,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ) -> Optional[str]:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.previous_state

    def get_states(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT
    ) -> list[str]:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        return magazine.states

    def set_state(
        self,
        state: str,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        data: Optional[dict] = None
    ) -> None:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)
        self._process_transition(
            magazine=magazine,
            source_state=magazine.state,
            destination_state=state,
            chat_id=chat_id,
            user_id=user_id,
            data=data
        )

    def reset_state(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        data: Optional[dict] = None
    ) -> None:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)
        context = StateContext(
            deps=self._deps,
            chat_id=chat_id,
            user_id=user_id,
            data=data
        )

        for hook in self._enter_hooks.get(magazine.state, []):
            hook(context)

    def set_previous_state(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, FromContext, None] = OPTIONAL_FROM_CONTEXT,
        data: Optional[dict] = None
    ) -> None:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._load_magazine(chat_id=chat_id, user_id=user_id)

        if magazine.previous_state is None:
            raise PreviousStateNotFoundError(
                f"No previous state for chat_id={chat_id}, user_id={user_id}!"
            )

        self._process_transition(
            magazine=magazine,
            source_state=magazine.state,
            destination_state=magazine.previous_state,
            chat_id=chat_id,
            user_id=user_id,
            data=data
        )

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

    def _process_transition(
        self,
        magazine: StateMagazine,
        source_state: str,
        destination_state: str,
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        data: Optional[dict] = None
    ) -> None:
        context = StateContext(
            deps=self._deps,
            chat_id=chat_id,
            user_id=user_id,
            data=data
        )

        for hook in self._exit_hooks.get(source_state, []):
            hook(context)

        magazine.set_state(destination_state)
        self._save_magazine(magazine, chat_id=chat_id, user_id=user_id)

        for hook in self._enter_hooks.get(destination_state, []):
            hook(context)


def _get_chat_id_and_user_id(
    chat_id: Union[int, FromContext],
    user_id: Union[int, FromContext, None]
) -> tuple[int, Optional[int]]:
    if isinstance(chat_id, FromContext):
        chat_id = get_event_value("chat_id", optional=chat_id.optional)

    if isinstance(user_id, FromContext):
        user_id = get_event_value("user_id", optional=user_id.optional)

    return chat_id, user_id


def _get_event(event: Union[Event, FromContext, None]) -> Optional[Event]:
    if isinstance(event, FromContext):
        event = event_context.get()

    return event
