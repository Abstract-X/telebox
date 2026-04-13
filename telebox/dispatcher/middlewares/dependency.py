from typing import Optional

from telebox.bot.bot import Bot
from telebox.dispatcher.flows.manager import FlowManager
from telebox.dispatcher.state_machine import StateMachine
from telebox.dispatcher.middleware import Middleware
from telebox.ui.ui import UI


class DependencyMiddleware(Middleware):
    def __init__(
        self,
        bot: Optional[Bot] = None,
        ui: Optional[UI] = None,
        state_machine: Optional[StateMachine] = None,
        flow_manager: Optional[FlowManager] = None,
        **kwargs
    ) -> None:
        self._bot = bot
        self._ui = ui
        self._state_machine = state_machine
        self._flow_manager = flow_manager
        self._kwargs = kwargs

    def on_pre_process(self, ctx) -> None:
        ctx.bot = self._bot
        ctx.ui = self._ui
        ctx.state_machine = self._state_machine
        ctx.flow_manager = self._flow_manager

        for name, value in self._kwargs.items():
            setattr(ctx, name, value)
