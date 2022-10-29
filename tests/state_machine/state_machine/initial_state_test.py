from telebox import StateMachine
from telebox.state_machine.storages import MemoryStateStorage
from tests.state_machine.state_machine.helpers import InitialState


def test() -> None:
    initial_state = InitialState()
    machine = StateMachine(initial_state, MemoryStateStorage())

    assert machine.initial_state is initial_state
