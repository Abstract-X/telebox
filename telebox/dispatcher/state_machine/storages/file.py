import json
from pathlib import Path
from typing import Optional, Union, Any
from threading import Lock
import uuid

from telebox.dispatcher.state_machine.storage import AbstractStateStorage


class FileStateStorage(AbstractStateStorage):
    def __init__(self, path: Union[str, Path]):
        self._path = Path(path).resolve()
        self._lock = Lock()

    def load_state_ids(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[list[int]]:
        key = _get_states_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            content = self._load_content()

            return content["states"].get(key, {}).get("state_ids")

    def load_flow_state_ids(
        self,
        *,
        flow_id: int
    ) -> Optional[list[int]]:
        key = _get_flow_states_key(flow_id=flow_id)

        with self._lock:
            content = self._load_content()

            return content["flow_states"].get(key)

    def save_state_transition(
        self,
        state_ids: list[int],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        key = _get_states_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            content = self._load_content()
            content["states"][key] = {
                "state_ids": state_ids,
                "input_flow_id": None
            }
            self._save_content(content)

    def save_flow_state_transition(
        self,
        state_ids: list[int],
        *,
        flow_id: int,
        chat_id: int,
        user_id: Optional[int] = None,
        input_flow_id: Optional[int] = None
    ) -> None:
        flow_states_key = _get_flow_states_key(flow_id=flow_id)
        states_key = _get_states_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            content = self._load_content()
            content["flow_states"][flow_states_key] = state_ids
            content["states"].setdefault(states_key, {"state_ids": []})["input_flow_id"] = input_flow_id
            self._save_content(content)

    def load_current_state_ids(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[list[int]]:
        states_key = _get_states_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            content = self._load_content()
            input_flow_id = content["states"].get(states_key, {}).get("input_flow_id")

            if input_flow_id is not None:
                flow_states_key = _get_flow_states_key(flow_id=input_flow_id)
                state_ids = content["flow_states"].get(flow_states_key)
            else:
                state_ids = content["states"].get(states_key, {}).get("state_ids")

            return state_ids

    def load_input_flow_id(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[int]:
        key = _get_states_key(chat_id=chat_id, user_id=user_id)

        with self._lock:
            content = self._load_content()

            return content["states"].get(key, {}).get("input_flow_id")

    def _save_content(self, content: dict[str, Any]) -> None:
        temp_path = self._path.parent / f".{uuid.uuid4().hex}.json"

        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(content, file, indent=4, sort_keys=True)

            temp_path.replace(self._path)
        finally:
            temp_path.unlink(missing_ok=True)

    def _load_content(self) -> dict[str, Any]:
        try:
            with self._path.open(encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {
                "states": {},
                "flow_states": {}
            }


def _get_states_key(*, chat_id: int, user_id: Optional[int] = None) -> str:
    if user_id is None:
        return str(chat_id)

    return f"{chat_id}:{user_id}"


def _get_flow_states_key(*, flow_id: int) -> str:
    return str(flow_id)
