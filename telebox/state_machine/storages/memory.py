from typing import Optional
from threading import Lock

from telebox.state_machine.storage import AbstractStateStorage


StateDict = dict[
    int,
    dict[
        int,
        list[str]
    ]
]


class MemoryStateStorage(AbstractStateStorage):
    def __init__(self):
        self._states: StateDict = {}
        self._lock = Lock()

    def save_states(
        self,
        states: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            try:
                self._states[chat_id][user_id] = states[:]
            except KeyError:
                self._states[chat_id] = {
                    user_id: states[:]
                }

    def load_states(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        with self._lock:
            try:
                return self._states[chat_id][user_id][:]
            except KeyError:
                return []
