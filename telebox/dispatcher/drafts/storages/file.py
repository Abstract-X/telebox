from pathlib import Path
from typing import Optional, Union
from threading import Lock

from telebox.serialization import get_serialized_data, get_deserialized_data
from telebox.dispatcher.drafts.storage import AbstractDraftStorage, Value


class FileDraftStorage(AbstractDraftStorage):
    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).resolve()
        self._temp_path = self._path.with_suffix(".temp")
        self._lock = Lock()

    def save_draft(
        self,
        draft: dict[str, Value],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            drafts = self._load_drafts()
            drafts[key] = draft
            self._save_drafts(drafts)

    def load_draft(
        self,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> dict[str, Value]:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            stored_drafts = self._load_drafts()

            return stored_drafts.get(key, {})

    def clear_draft(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            drafts = self._load_drafts()
            draft = drafts.pop(key, None)

            if draft is not None:
                self._save_drafts(drafts)

    def _save_drafts(self, drafts: dict[str, dict[str, Value]]) -> None:
        with self._temp_path.open("w", encoding="utf-8") as stream:
            stream.write(
                get_serialized_data(drafts)
            )

        self._temp_path.replace(self._path)

    def _load_drafts(self) -> dict[str, dict[str, Value]]:
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
