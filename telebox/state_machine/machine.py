from typing import Optional

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
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
from telebox.typing import Event


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

        for i in (source_state, destination_state):
            if i not in self._state_manager.states:
                self._state_manager.add_state(i)

    def get_state(self, *, chat_id: int, user_id: Optional[int] = None) -> State:
        magazine = self._state_manager.load_magazine(chat_id=chat_id, user_id=user_id)

        return self._state_manager.get_state(magazine.current_state)

    def set_next_state(
        self,
        event: Event,
        handler: AbstractEventHandler,
        direction: Optional[str] = None,
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
            chat_id=chat_id,
            user_id=user_id
        )

    def set_previous_state(
        self,
        event: Event,
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
            chat_id=chat_id,
            user_id=user_id
        )

    def set_state(
        self,
        state: State,
        event: Event,
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
            chat_id=chat_id,
            user_id=user_id
        )

    def reset_state(
        self,
        event: Event,
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        with_exit: bool = True
    ) -> None:
        state = self.get_state(chat_id=chat_id, user_id=user_id)

        if with_exit:
            state.process_exit(event)

        state.process_enter(event)

    def _process_transition(
        self,
        event: Event,
        magazine: StateMagazine,
        source_state: State,
        destination_state: State,
        *,
        chat_id: int,
        user_id: int
    ) -> None:
        source_state.process_exit(event)
        destination_state.process_enter(event)
        magazine.set_state(str(destination_state))
        self._state_manager.save_magazine(magazine, chat_id=chat_id, user_id=user_id)
