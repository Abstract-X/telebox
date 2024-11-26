from __future__ import annotations
import logging
from threading import Event
from signal import signal, Signals, SIGINT, SIGTERM
from typing import TYPE_CHECKING, Iterable
import sys

if TYPE_CHECKING:
    from telebox.dispatcher.dispatcher import Dispatcher


logger = logging.getLogger(__name__)


def set_signal_handler(
    dispatcher: Dispatcher,
    *,
    signals: Iterable[int] = (SIGINT, SIGTERM)
) -> Event:
    stop_event = Event()

    def process_shutdown(signal_number: int, _) -> None:
        signal_name = Signals(signal_number).name
        logger.info("Signal handler called with signal %r (%r).", signal_name, signal_number)
        stop_event.set()

        if dispatcher.polling_is_used:
            dispatcher.stop_polling()
        elif dispatcher.server_is_used:
            dispatcher.stop_server()
        else:
            sys.exit()

    for i in signals:
        signal(i, process_shutdown)

    return stop_event
