from typing import Optional, Union, Iterable

from telebox.state_machine.state import State
from telebox.state_machine.storage import AbstractStateStorage
from telebox.state_machine.manager import StateManager
from telebox.state_machine.transition_scheme import TransitionScheme
from telebox.state_machine.magazine import StateMagazine
from telebox.state_machine.errors import (
    DestinationStateNotFoundError,
    NextStateNotFoundError,
    PreviousStateNotFoundError
)
from telebox.utils.deps import Deps
from telebox.dispatcher.context import Context, CONTEXT, OPTIONAL_CONTEXT, event_context, get_event_value
from telebox.dispatcher.type_hints import Event, Handler


TransitionDict = dict[State, dict[Handler, Union[State, dict[str, State]]]]


class StateMachine:
    def __init__(
        self,
        initial_state: State,
        states: Iterable[State],
        storage: AbstractStateStorage,
        deps: Deps
    ):
        self._deps = deps
        self._state_manager = StateManager(initial_state, storage)
        self.add_states(states)
        self._transition_scheme = TransitionScheme()

    @property
    def initial_state(self) -> State:
        return self._state_manager.initial_state

    @property
    def states(self) -> set[State]:
        return self._state_manager.states

    def add_states(self, states: Iterable[State]) -> None:
        for i in states:
            self._state_manager.add_state(i)

    def add_transition(
        self,
        source_state: State,
        destination_state: State,
        handler: Handler,
        direction: Optional[str] = None
    ) -> None:
        self._transition_scheme.add_transition(
            source_state=source_state,
            destination_state=destination_state,
            handler=handler,
            direction=direction
        )
        self.add_states((source_state, destination_state))

    def add_transitions(self, transitions: TransitionDict) -> None:
        for source_state in transitions:
            for handler, destination_item in transitions[source_state].items():
                if isinstance(destination_item, dict):
                    for direction, destination_state in destination_item.items():
                        self.add_transition(source_state, destination_state, handler, direction)
                else:
                    self.add_transition(source_state, destination_item, handler)

    def check_state(self, state: State) -> bool:
        return self._state_manager.check_state(state)

    def check_transition(
        self,
        source_state: State,
        destination_state: State,
        handler: Handler,
        direction: Optional[str] = None
    ) -> bool:
        return self._transition_scheme.check_transition(
            source_state,
            destination_state,
            handler,
            direction
        )

    def get_state(
        self,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT
    ) -> State:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        return self._state_manager.get_state(magazine.current_state)

    def get_states(
        self,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT
    ) -> list[State]:
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)

        return [
            self._state_manager.get_state(i)
            for i in self._state_manager.load_magazine(
                chat_id=chat_id,
                user_id=user_id
            )
        ]

    def set_next_state(
        self,
        handler: Handler,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        event: Union[Event, Context, None] = OPTIONAL_CONTEXT,
        data: Optional[dict] = None,
        direction: Optional[str] = None
    ) -> None:
        data = data or {}
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        event = _get_event(event)
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)
        current_state = self._state_manager.get_state(magazine.current_state)

        try:
            next_state = self._transition_scheme.get_destination_state(
                source_state=current_state,
                handler=handler,
                direction=direction
            )
        except DestinationStateNotFoundError as error:
            raise NextStateNotFoundError(
                "Transition to a next state has not been set "
                "({source_state=}, {handler=}, {direction=})!",
                source_state=error.source_state,
                handler=error.handler,
                direction=error.direction
            ) from None

        self._process_transition(
            magazine=magazine,
            source_state=current_state,
            destination_state=next_state,
            chat_id=chat_id,
            user_id=user_id,
            event=event,
            data=data
        )

    def set_previous_state(
        self,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        event: Union[Event, Context, None] = OPTIONAL_CONTEXT,
        data: Optional[dict] = None
    ) -> None:
        data = data or {}
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        event = _get_event(event)
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)
        current_state = self._state_manager.get_state(magazine.current_state)

        if magazine.previous_state is None:
            raise PreviousStateNotFoundError(
                "A previous state cannot be found because the current "
                "state is the initial state!",
                current_state=current_state
            )

        previous_state = self._state_manager.get_state(magazine.previous_state)
        self._process_transition(
            magazine=magazine,
            source_state=current_state,
            destination_state=previous_state,
            chat_id=chat_id,
            user_id=user_id,
            event=event,
            data=data
        )

    def set_state(
        self,
        state: State,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        event: Union[Event, Context, None] = OPTIONAL_CONTEXT,
        data: Optional[dict] = None
    ) -> None:
        data = data or {}
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        event = _get_event(event)
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)
        current_state = self._state_manager.get_state(magazine.current_state)
        self._process_transition(
            magazine=magazine,
            source_state=current_state,
            destination_state=state,
            chat_id=chat_id,
            user_id=user_id,
            event=event,
            data=data
        )

    def reset_state(
        self,
        *,
        chat_id: Union[int, Context] = CONTEXT,
        user_id: Union[int, Context, None] = OPTIONAL_CONTEXT,
        event: Union[Event, Context, None] = OPTIONAL_CONTEXT,
        data: Optional[dict] = None,
        with_exit: bool = True
    ) -> None:
        data = data or {}
        chat_id, user_id = _get_chat_id_and_user_id(chat_id=chat_id, user_id=user_id)
        event = _get_event(event)
        state = self.get_state(chat_id=chat_id, user_id=user_id)

        if with_exit:
            state.process_exit(
                deps=self._deps,
                chat_id=chat_id,
                user_id=user_id,
                event=event,
                data=data
            )

        state.process_enter(
            deps=self._deps,
            chat_id=chat_id,
            user_id=user_id,
            event=event,
            data=data
        )

    def _process_transition(
        self,
        magazine: StateMagazine,
        source_state: State,
        destination_state: State,
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        event: Optional[Event] = None,
        data: Optional[dict] = None
    ) -> None:
        data = data or {}
        source_state.process_exit(
            deps=self._deps,
            chat_id=chat_id,
            user_id=user_id,
            event=event,
            data=data
        )
        destination_state.process_enter(
            deps=self._deps,
            chat_id=chat_id,
            user_id=user_id,
            event=event,
            data=data
        )
        magazine.set_state(str(destination_state))
        self._state_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)


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
