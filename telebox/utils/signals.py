from __future__ import annotations
import logging
from signal import signal, Signals, SIGINT, SIGTERM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telebox.dispatcher.dispatcher import Dispatcher


logger = logging.getLogger(__name__)


def set_signal_handler(dispatcher: Dispatcher) -> None:
    def process_shutdown(signal_number: int, _) -> None:
        signal_name = Signals(signal_number).name
        logger.info("Signal handler called with signal %r (%r).", signal_name, signal_number)

        if dispatcher.polling_is_used:
            dispatcher.stop_polling()
        elif dispatcher.server_is_used:
            dispatcher.stop_server()

    for i in (SIGINT, SIGTERM):
        signal(i, process_shutdown)
