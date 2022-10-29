import pytest

from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
from telebox.state_machine.errors import StateNameExistsError, StateExistsError
from tests.state_machine.state_machine.helpers import InitialState, FooState


def test() -> None:
    machine = StateMachine(InitialState(), MemoryStateStorage())
    foo_state = FooState()
    machine.add_state(foo_state)

    assert machine.check_state(foo_state)


def test_existing_state() -> None:
    machine = StateMachine(InitialState(), MemoryStateStorage())
    foo_state = FooState()
    machine.add_state(foo_state)

    with pytest.raises(StateExistsError):
        machine.add_state(foo_state)


def test_state_with_existing_name() -> None:
    machine = StateMachine(InitialState(), MemoryStateStorage())
    machine.add_state(
        FooState()
    )

    with pytest.raises(StateNameExistsError):
        machine.add_state(
            FooState()
        )
