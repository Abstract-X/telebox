from pathlib import Path
from typing import Optional, Union, Any
from threading import Lock
import uuid

from telebox.dispatcher.state_machine.storage import AbstractStateBundleStorage
from telebox.utils import get_serialized_data, get_deserialized_data


class FileStateBundleStorage(AbstractStateBundleStorage):
    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).resolve()
        self._lock = Lock()

    def save(
        self,
        magazine: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        flow_id: Optional[int] = None
    ) -> None:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            bundles = self._load_all()
            bundles[key] = {
                "magazine": magazine,
                "flow_id": flow_id
            }
            self._save_all(bundles)

    def load(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> tuple[Optional[list[str]], Optional[int]]:
        key = _get_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            bundles = self._load_all()
            bundle = bundles.get(key)

            if not bundle:
                return None, None

            return bundle["magazine"], bundle["flow_id"]

    def _save_all(self, bundles: dict[str, dict[str, Any]]) -> None:
        temp_path = self._path.parent / f".{uuid.uuid4().hex}.json"

        try:
            with temp_path.open("w", encoding="utf-8") as file:
                file.write(
                    get_serialized_data(bundles).decode("utf-8")
                )

            temp_path.replace(self._path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _load_all(self) -> dict[str, dict[str, Any]]:
        try:
            with self._path.open(encoding="utf-8") as file:
                return get_deserialized_data(
                    file.read()
                )
        except FileNotFoundError:
            return {}


def _get_key(*, chat_id: int, user_id: Optional[int] = None) -> str:
    if user_id is None:
        return str(chat_id)

    return f"{chat_id}:{user_id}"
