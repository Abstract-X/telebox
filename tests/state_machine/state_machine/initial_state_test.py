from telebox import StateMachine, State
from telebox.state_machine.storages import MemoryStateStorage


def test() -> None:
    state = State()
    storage = MemoryStateStorage()
    machine = StateMachine(state, storage)

    assert machine.initial_state is state
