from __future__ import annotations
from typing import Optional, Union, Any, Iterable, TYPE_CHECKING

from telebox.state_machine.state import State
from telebox.state_machine.storages.storage import AbstractStateStorage
from telebox.state_machine.manager import StateManager
from telebox.state_machine.transition_scheme import TransitionScheme
from telebox.state_machine.magazine import StateMagazine
from telebox.state_machine.errors import (
    DestinationStateNotFoundError,
    NextStateNotFoundError,
    PreviousStateNotFoundError
)
from telebox.dispatcher.handlers.event import AbstractEventHandler
if TYPE_CHECKING:
    from telebox.dispatcher.typing import Event


TransitionDict = dict[State, dict[AbstractEventHandler, Union[State, dict[str, State]]]]


class StateMachine:

    def __init__(self, initial_state: State, storage: AbstractStateStorage):
        self._state_manager = StateManager(initial_state, storage)
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
        handler: AbstractEventHandler,
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
        handler: AbstractEventHandler,
        direction: Optional[str] = None
    ) -> bool:
        return self._transition_scheme.check_transition(
            source_state,
            destination_state,
            handler,
            direction
        )

    def get_state(self, *, chat_id: int, user_id: Optional[int] = None) -> State:
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        return self._state_manager.get_state(magazine.current_state)

    def set_next_state(
        self,
        handler: AbstractEventHandler,
        event: Optional[Event] = None,
        direction: Optional[str] = None,
        data: Any = None,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
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
            event=event,
            magazine=magazine,
            source_state=current_state,
            destination_state=next_state,
            data=data,
            chat_id=chat_id,
            user_id=user_id
        )

    def set_previous_state(
        self,
        event: Optional[Event] = None,
        data: Any = None,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
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
            event=event,
            magazine=magazine,
            source_state=current_state,
            destination_state=previous_state,
            data=data,
            chat_id=chat_id,
            user_id=user_id
        )

    def set_state(
        self,
        state: State,
        event: Optional[Event] = None,
        data: Any = None,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)
        current_state = self._state_manager.get_state(magazine.current_state)
        self._process_transition(
            event=event,
            magazine=magazine,
            source_state=current_state,
            destination_state=state,
            data=data,
            chat_id=chat_id,
            user_id=user_id
        )

    def reset_state(
        self,
        event: Optional[Event] = None,
        data: Any = None,
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        with_exit: bool = True
    ) -> None:
        state = self.get_state(chat_id=chat_id, user_id=user_id)

        if with_exit:
            state.process_exit(chat_id, user_id, event, data)

        state.process_enter(chat_id, user_id, event, data)

    def _process_transition(
        self,
        magazine: StateMagazine,
        source_state: State,
        destination_state: State,
        event: Optional[Event] = None,
        data: Any = None,
        *,
        chat_id: int,
        user_id: int
    ) -> None:
        source_state.process_exit(chat_id, user_id, event, data)
        destination_state.process_enter(chat_id, user_id, event, data)
        magazine.set_state(str(destination_state))
        self._state_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
