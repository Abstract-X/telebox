from telebox.dispatcher.filters.base.event import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.state_machine.state import State
from telebox.state_machine.state_machine import StateMachine


class StateFilter(AbstractEventFilter):

    def __init__(self, *states: State, state_machine: StateMachine):
        self._states = set(states)
        self._state_machine = state_machine

    def check(self, event: Message) -> bool:
        state = self._state_machine.get_state(chat_id=event.chat_id, user_id=event.user_id)

        return state in self._states
