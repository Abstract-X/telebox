from unittest.mock import Mock

import pytest

from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
from telebox.state_machine.errors import StateNotFoundError
from tests.state_machine.state_machine.helpers import InitialState, FooState


def test(chat_id: int, user_id: int) -> None:
    initial_state = InitialState()
    machine = StateMachine(initial_state, MemoryStateStorage())

    assert machine.get_state(chat_id=chat_id, user_id=user_id) is initial_state

    foo_state = FooState()
    machine.add_state(foo_state)
    machine.set_state(state=foo_state, event=Mock(), chat_id=chat_id, user_id=user_id)

    assert machine.get_state(chat_id=chat_id, user_id=user_id) is foo_state


def test_not_added_state(chat_id: int, user_id: int) -> None:
    machine = StateMachine(InitialState(), MemoryStateStorage())
    machine.set_state(state=FooState(), event=Mock(), chat_id=chat_id, user_id=user_id)

    with pytest.raises(StateNotFoundError):
        machine.get_state(chat_id=chat_id, user_id=user_id)
