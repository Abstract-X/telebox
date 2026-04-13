from pathlib import Path
from typing import Optional, Union
from threading import Lock
import uuid

from telebox.dispatcher.drafts.storage import AbstractDraftStorage, Value
from telebox.utils import get_serialized_data, get_deserialized_data


class FileDraftStorage(AbstractDraftStorage):
    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).resolve()
        self._lock = Lock()

    def _save(
        self,
        data: bytes,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            drafts = self._load_all()
            drafts[key] = get_deserialized_data(data)
            self._save_all(drafts)

    def _load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[bytes]:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            drafts = self._load_all()
            data = drafts.get(key)

            if data is not None:
                return get_serialized_data(data)

    def delete(self, *, chat_id: int, user_id: Optional[int] = None) -> None:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            drafts = self._load_all()
            drafts.pop(key, None)
            self._save_all(drafts)

    def _save_all(self, drafts: dict[str, dict[str, Value]]) -> None:
        temp_path = self._path.parent / f".{uuid.uuid4().hex}.json"

        try:
            with temp_path.open("wb") as file:
                file.write(
                    get_serialized_data(drafts)
                )

            temp_path.replace(self._path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _load_all(self) -> dict[str, dict[str, Value]]:
        try:
            with self._path.open("rb") as file:
                return get_deserialized_data(
                    file.read()
                )
        except FileNotFoundError:
            return {}


def _get_key(*, chat_id: int, user_id: Optional[int] = None) -> str:
    if user_id is None:
        return str(chat_id)

    return f"{chat_id}:{user_id}"
