from typing import Optional, Any

from telebox.state_machine.machine import StateMachine
from telebox.utils.context.vars import event_context, event_handler_context


class ContextStateMachine:

    def __init__(self, machine: StateMachine):
        self._machine = machine

    def set_next_state(self, direction: Optional[str] = None, data: Any = None) -> None:
        event = event_context.get()
        self._machine.set_next_state(
            event=event,
            handler=event_handler_context.get(),
            direction=direction,
            data=data,
            chat_id=event.chat_id,
            user_id=event.user_id
        )

    def set_previous_state(self, data: Any = None) -> None:
        event = event_context.get()
        self._machine.set_previous_state(
            event=event,
            data=data,
            chat_id=event.chat_id,
            user_id=event.user_id
        )

    def reset_state(self, data: Any = None, *, with_exit: bool = True) -> None:
        event = event_context.get()
        self._machine.reset_state(
            event=event,
            chat_id=event.chat_id,
            user_id=event.user_id,
            with_exit=with_exit
        )
