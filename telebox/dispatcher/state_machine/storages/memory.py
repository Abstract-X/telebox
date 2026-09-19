from dataclasses import dataclass, field
from typing import Optional
from threading import Lock

from telebox.dispatcher.state_machine.storage import AbstractStateStorage


@dataclass
class StateRecord:
    state_ids: list[int] = field(default_factory=list)
    input_flow_id: Optional[int] = None


@dataclass
class FlowStateRecord:
    state_ids: list[int]


class MemoryStateStorage(AbstractStateStorage):
    def __init__(self):
        self._state_records: dict[tuple[int, Optional[int]], StateRecord] = {}
        self._flow_state_records: dict[int, FlowStateRecord] = {}
        self._lock = Lock()

    def load_state_ids(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[list[int]]:
        with self._lock:
            record = self._state_records.get((chat_id, user_id))

            if record is not None:
                return record.state_ids

    def load_flow_state_ids(
        self,
        *,
        flow_id: int
    ) -> Optional[list[int]]:
        with self._lock:
            record = self._flow_state_records.get(flow_id)

            if record is not None:
                return record.state_ids

    def save_state_transition(
        self,
        state_ids: list[int],
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> None:
        state_ids = state_ids[:]

        with self._lock:
            record = self._state_records.get((chat_id, user_id))

            if record is not None:
                record.state_ids = state_ids
                record.input_flow_id = None
            else:
                self._state_records[(chat_id, user_id)] = StateRecord(state_ids=state_ids)

    def save_flow_state_transition(
        self,
        state_ids: list[int],
        *,
        flow_id: int,
        chat_id: int,
        user_id: Optional[int] = None,
        input_flow_id: Optional[int] = None
    ) -> None:
        state_ids = state_ids[:]

        with self._lock:
            flow_state_record = self._flow_state_records.get(flow_id)

            if flow_state_record is not None:
                flow_state_record.state_ids = state_ids
            else:
                self._flow_state_records[flow_id] = FlowStateRecord(state_ids=state_ids)

            state_record = self._state_records.get((chat_id, user_id))

            if state_record is not None:
                state_record.input_flow_id = input_flow_id
            else:
                self._state_records[(chat_id, user_id)] = StateRecord(input_flow_id=input_flow_id)

    def load_current_state_ids(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[list[int]]:
        state_ids = None

        with self._lock:
            state_record = self._state_records.get((chat_id, user_id))

            if state_record is not None:
                state_ids = state_record.state_ids

                if state_record.input_flow_id is not None:
                    state_ids = self._flow_state_records[state_record.input_flow_id].state_ids

            if state_ids is not None:
                return state_ids[:]

    def load_input_flow_id(
        self,
        *,
        chat_id: int,
        user_id: Optional[int] = None
    ) -> Optional[int]:
        with self._lock:
            record = self._state_records.get((chat_id, user_id))

            if record is not None:
                return record.input_flow_id
