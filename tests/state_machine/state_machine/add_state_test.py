from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
from tests.state_machine.state_machine.helpers import InitialState, FooState


def test() -> None:
    machine = StateMachine(InitialState(), MemoryStateStorage())
    foo_state = FooState()
    machine.add_state(foo_state)

    assert machine.check_state(foo_state)
