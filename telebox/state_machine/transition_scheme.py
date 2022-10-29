from typing import Optional

from telebox.state_machine.state import State
from telebox.dispatcher.handlers.event import AbstractEventHandler
from telebox.state_machine.errors import (
    TransitionExistsError,
    DestinationStateNotFoundError
)


TransitionDict = dict[
    State,
    dict[
        AbstractEventHandler,
        dict[
            Optional[str],
            State
        ]
    ]
]


class TransitionScheme:

    def __init__(self):
        self._transitions: TransitionDict = {}

    def add_transition(
        self,
        source_state: State,
        destination_state: State,
        handler: AbstractEventHandler,
        direction: Optional[str] = None
    ) -> None:
        if self._check_destination_state(source_state, handler, direction):
            raise TransitionExistsError(
                "Transition already exists ({source_state=}, {handler=}, {direction=})!",
                source_state=source_state,
                handler=handler,
                direction=direction
            )

        source_states = self._transitions.setdefault(source_state, {})
        handlers = source_states.setdefault(handler, {})
        handlers[direction] = destination_state

    def check_transition(
        self,
        source_state: State,
        destination_state: State,
        handler: AbstractEventHandler,
        direction: Optional[str] = None
    ) -> bool:
        try:
            return self._transitions[source_state][handler][direction] is destination_state
        except KeyError:
            return False

    def get_destination_state(
        self,
        source_state: State,
        handler: AbstractEventHandler,
        direction: Optional[str] = None
    ) -> State:
        try:
            return self._transitions[source_state][handler][direction]
        except KeyError:
            raise DestinationStateNotFoundError(
                "Destination state not found ({source_state=}, {handler=}, {direction=})!",
                source_state=source_state,
                handler=handler,
                direction=direction
            ) from None

    def _check_destination_state(
        self,
        source_state: State,
        handler: AbstractEventHandler,
        direction: Optional[str] = None
    ) -> bool:
        try:
            self._transitions[source_state][handler][direction]
        except KeyError:
            return False

        return True
