import logging
from queue import Queue
from typing import Optional, Union, TYPE_CHECKING
from threading import Event
import contextlib
import time

from httpx import TimeoutException

from telebox.bot.types import Update
from telebox.dispatcher.listener import AbstractListener
if TYPE_CHECKING:
    from telebox.bot.bot import Bot


logger = logging.getLogger(__name__)


class LongPollingListener(AbstractListener):
    def __init__(
        self,
        bot: "Bot",
        *,
        error_delay: Union[int, float] = 5,
        limit: Optional[int] = None,
        timeout: Optional[int] = 10,
        allowed_updates: Optional[list[str]] = None
    ):
        if error_delay < 0:
            raise ValueError("Error delay seconds cannot be negative!")

        self._bot = bot
        self._error_delay = error_delay
        self._limit = limit
        self._timeout = timeout
        self._request_timeout = timeout + 1 if timeout else None
        self._allowed_updates = allowed_updates
        self._stop_event = Event()

    def run(self, updates: Queue[Update]) -> None:
        offset_update_id = None

        with contextlib.suppress(KeyboardInterrupt):
            while not self._stop_event.is_set():
                try:
                    updates_ = self._bot.get_updates(
                        offset=offset_update_id,
                        limit=self._limit,
                        timeout=self._timeout,
                        allowed_updates=self._allowed_updates,
                        request_timeout=self._request_timeout
                    )
                except TimeoutException:
                    logger.error("Requesting updates timed out.")
                except Exception:  # noqa
                    logger.exception("An error occurred while receiving updates!")

                    for _ in range(self._error_delay):
                        if self._stop_event.is_set():
                            return

                        time.sleep(0.1)
                else:
                    for i in updates_:
                        updates.put(i)

                    if updates_:
                        offset_update_id = updates_[-1].update_id + 1

    def stop(self) -> None:
        self._stop_event.set()
