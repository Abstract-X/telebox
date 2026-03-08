from pathlib import Path
from typing import Optional, Union
from threading import Lock

from telebox.state_machine.storage import AbstractStateStorage
from telebox.serialization import get_serialized_data, get_deserialized_data


class FileStateStorage(AbstractStateStorage):
    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).resolve()
        self._temp_path = self._path.with_suffix(".temp")
        self._lock = Lock()

    def save_states(
        self,
        states: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            stored_states = self._load_states()
            stored_states[key] = states

            with self._temp_path.open("w", encoding="utf-8") as stream:
                stream.write(
                    get_serialized_data(stored_states)
                )

            self._temp_path.replace(self._path)

    def load_states(self, *, chat_id: int, user_id: Optional[int] = None) -> list[str]:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            stored_states = self._load_states()

            return stored_states.get(key, [])

    def _load_states(self) -> dict[str, list[str]]:
        try:
            with self._path.open(encoding="utf-8") as stream:
                return get_deserialized_data(
                    stream.read()
                )
        except FileNotFoundError:
            return {}


def _get_key(*, chat_id: int, user_id: Optional[int] = None) -> str:
    if user_id is None:
        return str(chat_id)

    return f"{chat_id}:{user_id}"
