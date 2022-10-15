from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.telegram_bot.types.types.message import Message
from telebox.state_machine.state import State
from telebox.state_machine.machine import StateMachine


class StateFilter(AbstractEventFilter):

    def __init__(self, *states: State, state_machine: StateMachine):
        self._states = set(states)
        self._state_machine = state_machine

    def get_value(self, event: Message) -> State:
        return self._state_machine.get_state(chat_id=event.chat_id, user_id=event.user_id)

    def check_value(self, value: State) -> bool:
        return value in self._states
