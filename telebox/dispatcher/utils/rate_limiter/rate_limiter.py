from typing import Optional

from telebox.dispatcher.utils.rate_limiter.rate_limit import RateLimit
from telebox.dispatcher.utils.rate_limiter.call_tracker import CallTracker


class RateLimiter:

    def __init__(self, limit: RateLimit):
        self.limit = limit
        self._call_tracker = CallTracker(
            chat_ttl_secs=limit.chat_limit_secs,
            user_ttl_secs=limit.user_limit_secs,
            chat_user_ttl_secs=limit.chat_user_limit_secs
        )
        self._processed_chat_ids: set[int] = set()
        self._processed_user_ids: set[int] = set()
        self._process_chat_user_ids: set[tuple[int, int]] = set()

    def process_call(self, chat_id: Optional[int], user_id: Optional[int]) -> bool:
        is_limited = False
        chat_id_is_not_none = chat_id is not None
        user_id_is_not_none = user_id is not None

        if chat_id_is_not_none and self.limit.check_chat_limit():
            chat_calls = self._call_tracker.get_chat_calls(chat_id)

            if chat_calls < self.limit.chat_limit_calls:
                self._processed_chat_ids.discard(chat_id)
            elif chat_calls == self.limit.chat_limit_calls:
                if chat_id not in self._processed_chat_ids:
                    self._processed_chat_ids.add(chat_id)
                    self.limit.process_chat_over_limit(chat_id)

                is_limited = True

        if user_id_is_not_none and self.limit.check_user_limit():
            user_calls = self._call_tracker.get_user_calls(user_id)

            if user_calls < self.limit.user_limit_calls:
                self._processed_user_ids.discard(user_id)
            elif user_calls == self.limit.user_limit_calls:
                if user_id not in self._processed_user_ids:
                    self._processed_user_ids.add(user_id)
                    self.limit.process_user_over_limit(user_id)

                is_limited = True

        if chat_id_is_not_none and user_id_is_not_none and self.limit.check_chat_user_limit():
            chat_user_calls = self._call_tracker.get_chat_user_calls(chat_id, user_id)
            chat_user_ids = (chat_id, user_id)

            if chat_user_calls < self.limit.chat_user_limit_calls:
                self._process_chat_user_ids.discard(chat_user_ids)
            elif chat_user_calls == self.limit.chat_user_limit_calls:
                if (chat_id, user_id) not in self._process_chat_user_ids:
                    self._process_chat_user_ids.add((chat_id, user_id))
                    self.limit.process_chat_user_over_limit(chat_id, user_id)

                is_limited = True

        if not is_limited:
            if chat_id_is_not_none:
                self._call_tracker.add_chat_call(chat_id)

            if user_id_is_not_none:
                self._call_tracker.add_user_call(user_id)

            if chat_id_is_not_none and user_id_is_not_none:
                self._call_tracker.add_chat_user_call(chat_id, user_id)

        return is_limited
