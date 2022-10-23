from typing import Optional

from telebox.state_machine.storages.storage import AbstractStateStorage


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

    def save_states(
        self,
        states: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        try:
            self._states[chat_id][user_id] = states[:]
        except KeyError:
            self._states[chat_id] = {
                user_id: states[:]
            }

    def load_states(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        try:
            return self._states[chat_id][user_id][:]
        except KeyError:
            return []
