from typing import Optional, Any

from telebox.state_machine.machine import StateMachine
from telebox.state_machine.state import State
from telebox.context.vars import event_context, event_handler_context
from telebox.context.utils import (
    get_event_chat_id,
    get_event_user_id
)


class ContextStateMachine:

    def __init__(self, machine: StateMachine):
        self._machine = machine

    def get_state(self, *, for_chat: bool = False) -> State:
        return self._machine.get_state(
            chat_id=get_event_chat_id(),
            user_id=None if for_chat else get_event_user_id()
        )

    def set_next_state(
        self,
        direction: Optional[str] = None,
        data: Any = None,
        *,
        for_chat: bool = False
    ) -> None:
        self._machine.set_next_state(
            event=event_context.get(),
            handler=event_handler_context.get(),
            direction=direction,
            data=data,
            chat_id=get_event_chat_id(),
            user_id=None if for_chat else get_event_user_id()
        )

    def set_previous_state(self, data: Any = None, *, for_chat: bool = False) -> None:
        self._machine.set_previous_state(
            event=event_context.get(),
            data=data,
            chat_id=get_event_chat_id(),
            user_id=None if for_chat else get_event_user_id()
        )

    def set_state(self, state: State, data: Any = None, *, for_chat: bool = False) -> None:
        self._machine.set_state(
            state=state,
            event=event_context.get(),
            data=data,
            chat_id=get_event_chat_id(),
            user_id=None if for_chat else get_event_user_id()
        )

    def reset_state(
        self,
        data: Any = None,
        *,
        with_exit: bool = True,
        for_chat: bool = False
    ) -> None:
        self._machine.reset_state(
            event=event_context.get(),
            data=data,
            chat_id=get_event_chat_id(),
            user_id=None if for_chat else get_event_user_id(),
            with_exit=with_exit
        )
