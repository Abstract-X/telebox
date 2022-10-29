from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
from tests.state_machine.state_machine.helpers import InitialState, FooState


def test() -> None:
    machine = StateMachine(InitialState(), MemoryStateStorage())
    foo_state = FooState()

    assert machine.check_state(foo_state) is False

    machine.add_state(foo_state)

    assert machine.check_state(foo_state) is True


def test_initial_state() -> None:
    initial_state = InitialState()
    machine = StateMachine(initial_state, MemoryStateStorage())

    assert machine.check_state(initial_state) is True
