from typing import Optional
from threading import Lock

from telebox.state_machine.storages.storage import AbstractStateStorage
from telebox.utils.serialization import get_serialized_data, get_deserialized_data


class JSONStateStorage(AbstractStateStorage):

    def __init__(self, path: str):
        self._path = path
        self._lock = Lock()

    def save_states(
        self,
        states: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        with self._lock:
            stored_states = self._load_stored_states()
            stored_states.setdefault(str(chat_id), {})[str(user_id)] = states

            with open(self._path, "w", encoding="UTF-8") as stream:
                stream.write(
                    get_serialized_data(stored_states)
                )

    def load_states(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        with self._lock:
            stored_states = self._load_stored_states()

            return stored_states.get(str(chat_id), {}).get(str(user_id), [])

    def _load_stored_states(self) -> dict[str, dict[str, list[str]]]:
        try:
            with open(self._path, encoding="UTF-8") as stream:
                return get_deserialized_data(
                    stream.read()
                )
        except FileNotFoundError:
            return {}
