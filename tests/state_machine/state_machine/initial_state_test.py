from telebox import StateMachine, State
from telebox.state_machine.storages import MemoryStateStorage


def test() -> None:
    state = State()
    machine = StateMachine(state, MemoryStateStorage())

    assert machine.initial_state is state
