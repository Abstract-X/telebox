import json
from typing import Optional, Union, Any
from pathlib import Path
from threading import Lock
import uuid

from telebox.dispatcher.flows.storage import AbstractFlowStorage


class FileFlowStorage(AbstractFlowStorage):
    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).resolve()
        self._lock = Lock()

    def create(self, *, chat_id: int, user_id: Optional[int] = None) -> int:
        with self._lock:
            content = self._load_content()
            flow_id = content["next_id"]
            content["next_id"] += 1
            flow_key = _get_flow_key(flow_id)
            content["flows"][flow_key] = {
                "chat_id": chat_id,
                "user_id": user_id,
                "data": {}
            }
            self._save_content(content)

            return flow_id

    def finish(self, flow_id: int) -> None:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()
            content["flows"].pop(flow_key, None)
            self._save_content(content)

    def save(self, flow_id: int, data: Optional[dict[str, Any]] = None) -> None:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()
            record = content["flows"].get(flow_key)

            if record is not None:
                record["data"] = data
                self._save_content(content)

    def load(self, flow_id: int) -> Optional[dict[str, Any]]:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()
            record = content["flows"].get(flow_key)

            if record is not None:
                return record["data"]

    def _save_content(self, content: dict[str, Any]) -> None:
        temp_path = self._path.parent / f".{uuid.uuid4().hex}.json"

        try:
            with temp_path.open("w") as file:
                json.dump(content, file, indent=4, sort_keys=True)

            temp_path.replace(self._path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _load_content(self) -> dict[str, Any]:
        try:
            with self._path.open() as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                "next_id": 1,
                "flows": {}
            }


def _get_flow_key(flow_id: int) -> str:
    return str(flow_id)
