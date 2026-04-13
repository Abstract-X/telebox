from typing import Optional, Union, Any
from pathlib import Path
from threading import Lock
import uuid

from telebox.dispatcher.flows.storage import AbstractFlowStorage
from telebox.utils import get_serialized_data, get_deserialized_data


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
                "chat_id": chat_id
            }

            if user_id is not None:
                content["flows"][flow_key]["user_id"] = user_id

            self._save_content(content)

            return flow_id

    def finish(self, flow_id: int) -> None:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()
            content["flows"].pop(flow_key, None)
            self._save_content(content)

    def check(self, flow_id: int) -> bool:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()

            return flow_key in content["flows"]

    def _save(self, flow_id: int, data: Optional[bytes] = None) -> None:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()

            if flow_key in content["flows"]:
                if data:
                    content["flows"][flow_key]["data"] = get_deserialized_data(data)
                else:
                    content["flows"][flow_key].pop("data", None)

                self._save_content(content)

    def _load(self, flow_id: int) -> Optional[bytes]:
        flow_key = _get_flow_key(flow_id)

        with self._lock:
            content = self._load_content()
            flow = content["flows"].get(flow_key)

            if flow:
                data = flow.get("data")

                return get_serialized_data(data) if data else None

    def _save_content(self, content: dict[str, Any]) -> None:
        temp_path = self._path.parent / f".{uuid.uuid4().hex}.json"

        try:
            with temp_path.open("wb") as file:
                file.write(
                    get_serialized_data(content)
                )

            temp_path.replace(self._path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _load_content(self) -> dict[str, Any]:
        try:
            with self._path.open() as file:
                return get_deserialized_data(
                    file.read()
                )
        except FileNotFoundError:
            return {
                "next_id": 1,
                "flows": {}
            }


def _get_flow_key(flow_id: int) -> str:
    return str(flow_id)
