from typing import Optional

import pytest

from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
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

    assert machine.check_transition(initial_state, foo_state, handler, direction) is False

    machine.add_transition(initial_state, foo_state, handler, direction)

    assert machine.check_transition(initial_state, foo_state, handler, direction) is True
