from typing import Optional

from telebox.state_machine.state import State
from telebox.state_machine.storages.base import AbstractStateStorage
from telebox.state_machine.magazine import StateMagazine
from telebox.state_machine.errors import (
    StateAlreadyExistsError,
    StateNameAlreadyExistsError,
    StateNotFoundError
)


class StateManager:

    def __init__(self, initial_state: State, storage: AbstractStateStorage):
        self._initial_state = initial_state
        self._storage = storage
        self._states: dict[str, State] = {}
        self.add_state(initial_state)

    @property
    def initial_state(self) -> State:
        return self._initial_state

    @property
    def states(self) -> set[State]:
        return set(self._states.values())

    def add_state(self, state: State) -> None:
        if state.name in self._states:
            raise StateNameAlreadyExistsError(
                "State name {state_name!r} already exists!",
                state_name=state.name
            )

        if state in self._states.values():
            raise StateAlreadyExistsError(
                "State {state!r} already exists!",
                state=state
            )

        self._states[state.name] = state

    def get_state(self, name: str) -> State:
        try:
            return self._states[name]
        except KeyError:
            raise StateNotFoundError(
                "State with name {state_name!r} not found!",
                state_name=name
            ) from None

    def load_magazine(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> StateMagazine:
        states = self._storage.load(chat_id=chat_id, user_id=user_id)

        if not states:
            states = [str(self._initial_state)]

        return StateMagazine(states)

    def save_magazine(
        self,
        magazine: StateMagazine,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        self._storage.save(list(magazine), chat_id=chat_id, user_id=user_id)
