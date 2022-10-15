from typing import Optional
from threading import Lock

import ujson

from telebox.state_machine.storages.storage import AbstractStateStorage


class FileStateStorage(AbstractStateStorage):

    def __init__(self, path: str):
        self._path = path
        self._lock = Lock()

    def save(self, states: list[str], *, chat_id: int, user_id: Optional[int] = None) -> None:
        with self._lock:
            stored_states = self._load_stored_states()
            stored_states.setdefault(str(chat_id), {})[str(user_id)] = states

            with open(self._path, "w", encoding="UTF-8") as stream:
                ujson.dump(stored_states, stream)

    def load(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        with self._lock:
            stored_states = self._load_stored_states()

            return stored_states.get(str(chat_id), {}).get(str(user_id), [])

    def _load_stored_states(self) -> dict[str, dict[str, list[str]]]:
        try:
            with open(self._path, encoding="UTF-8") as stream:
                return ujson.load(stream)
        except FileNotFoundError:
            return {}
