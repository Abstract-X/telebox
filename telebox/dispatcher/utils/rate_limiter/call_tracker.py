from typing import Union
from collections import deque
from threading import Lock
import time


class CallTracker:

    def __init__(
        self,
        *,
        chat_ttl_secs: Union[int, float, None] = None,
        user_ttl_secs: Union[int, float, None] = None,
        chat_user_ttl_secs: Union[int, float, None] = None
    ):
        self._chat_ttl_secs = chat_ttl_secs
        self._user_ttl_secs = user_ttl_secs
        self._chat_user_ttl_secs = chat_user_ttl_secs
        self._chat_call_times: dict[int, deque[float]] = {}
        self._user_call_times: dict[int, deque[float]] = {}
        self._chat_user_call_times: dict[int, dict[int, deque[float]]] = {}
        self._chat_call_time_lock = Lock()
        self._user_call_time_lock = Lock()
        self._chat_user_call_time_lock = Lock()

    def add_chat_call(self, chat_id: int) -> None:
        with self._chat_call_time_lock:
            self._chat_call_times.setdefault(chat_id, deque()).append(time.monotonic())

    def add_user_call(self, user_id: int) -> None:
        with self._user_call_time_lock:
            self._user_call_times.setdefault(user_id, deque()).append(time.monotonic())

    def add_chat_user_call(self, chat_id: int, user_id: int) -> None:
        with self._chat_user_call_time_lock:
            users = self._chat_user_call_times.setdefault(chat_id, {})
            call_times = users.setdefault(user_id, deque())
            call_times.append(time.monotonic())

    def get_chat_calls(self, chat_id: int) -> int:
        with self._chat_call_time_lock:
            chat_call_times = self._chat_call_times.get(chat_id)

            if chat_call_times is not None:
                if self._chat_ttl_secs is not None:
                    _remove_expired_call_times(chat_call_times, self._chat_ttl_secs)

                    if not chat_call_times:
                        del self._chat_call_times[chat_id]

                return len(chat_call_times)

            return 0

    def get_user_calls(self, user_id: int) -> int:
        with self._user_call_time_lock:
            user_call_times = self._user_call_times.get(user_id)

            if user_call_times is not None:
                if self._user_ttl_secs is not None:
                    _remove_expired_call_times(user_call_times, self._user_ttl_secs)

                    if not user_call_times:
                        del self._user_call_times[user_id]

                return len(user_call_times)

            return 0

    def get_chat_user_calls(self, chat_id: int, user_id: int) -> int:
        with self._chat_user_call_time_lock:
            chat_user_calls = self._chat_user_call_times.get(chat_id, {}).get(user_id)

            if chat_user_calls is not None:
                if self._chat_user_ttl_secs is not None:
                    _remove_expired_call_times(chat_user_calls, self._chat_user_ttl_secs)

                    if not chat_user_calls:
                        del self._chat_user_call_times[chat_id][user_id]

                        if not self._chat_user_call_times[chat_id]:
                            del self._chat_call_times[chat_id]

                return len(chat_user_calls)

            return 0


def _remove_expired_call_times(call_times: deque[float], ttl_secs: Union[int, float]) -> None:
    current_time = time.monotonic()
    expired_calls = 0

    for i in call_times:
        if (current_time - i) > ttl_secs:
            expired_calls += 1
        else:
            break

    for _ in range(expired_calls):
        call_times.popleft()
