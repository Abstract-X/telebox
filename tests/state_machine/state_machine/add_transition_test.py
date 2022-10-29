from typing import Optional

import pytest

from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
from telebox.state_machine.errors import TransitionExistsError
from tests.state_machine.state_machine.helpers import InitialState, FooState, Handler


TEST_DIRECTION_DATA = (
    ("direction",),
    (
        (None,),
        ("direction",)
    )
)


@pytest.mark.parametrize(*TEST_DIRECTION_DATA)
def test(direction: Optional[str]) -> None:
    initial_state = InitialState()
    machine = StateMachine(initial_state, MemoryStateStorage())
    foo_state = FooState()
    handler = Handler()
    machine.add_transition(initial_state, foo_state, handler, direction)

    assert machine.check_transition(initial_state, foo_state, handler, direction)


@pytest.mark.parametrize(*TEST_DIRECTION_DATA)
def test_existing_transition(direction: Optional[str]) -> None:
    initial_state = InitialState()
    machine = StateMachine(initial_state, MemoryStateStorage())
    foo_state = FooState()
    handler = Handler()
    machine.add_transition(initial_state, foo_state, handler, direction)

    with pytest.raises(TransitionExistsError):
        machine.add_transition(initial_state, foo_state, handler, direction)
