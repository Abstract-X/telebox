from typing import Optional
from threading import Lock

from telebox.state_machine.storage import AbstractStateStorage


class MemoryStateStorage(AbstractStateStorage):
    def __init__(self):
        self._states: dict[tuple[int, Optional[int]], list[str]] = {}
        self._lock = Lock()

    def save_states(
        self,
        states: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            self._states[(chat_id, user_id)] = states[:]

    def load_states(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        with self._lock:
            states = self._states.get((chat_id, user_id))

            if states is not None:
                return states[:]

        return []
