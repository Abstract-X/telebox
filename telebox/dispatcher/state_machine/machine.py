from typing import Union, Callable, Collection, TYPE_CHECKING, Optional

from telebox.dispatcher.state_machine.errors import PreviousStateNotFoundError
from telebox.dispatcher.state_machine.history import StateHistory
from telebox.dispatcher.state_machine.storage import AbstractStateStorage
from telebox.context_values import (
    event_context_context,
    FromContext,
    FROM_CONTEXT, chat_id_context, user_id_context, OPTIONAL_FROM_CONTEXT
)
if TYPE_CHECKING:
    from telebox.dispatcher.context import EventContext


class StateMachine:
    def __init__(
        self,
        storage: AbstractStateStorage,
        input_flow_state_ids: Collection[int] = ()
    ):
        self._storage = storage
        self._input_flow_state_ids = frozenset(input_flow_state_ids or ())
        self._state_enter_hooks: dict[int, list[Callable[["EventContext"], None]]] = {}
        self._state_exit_hooks: dict[int, list[Callable[["EventContext"], None]]] = {}
        self._flow_state_enter_hooks: dict[int, list[Callable[["EventContext"], None]]] = {}
        self._flow_state_exit_hooks: dict[int, list[Callable[["EventContext"], None]]] = {}

    def add_state_enter_hook(self, state_id: int, hook: Callable[["EventContext"], None]) -> None:
        self._state_enter_hooks.setdefault(state_id, []).append(hook)

    def add_state_exit_hook(self, state_id: int, hook: Callable[["EventContext"], None]) -> None:
        self._state_exit_hooks.setdefault(state_id, []).append(hook)

    def add_flow_state_enter_hook(self, state_id: int, hook: Callable[["EventContext"], None]) -> None:
        self._flow_state_enter_hooks.setdefault(state_id, []).append(hook)

    def add_flow_state_exit_hook(self, state_id: int, hook: Callable[["EventContext"], None]) -> None:
        self._flow_state_exit_hooks.setdefault(state_id, []).append(hook)

    def get_state_history(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT
    ) -> StateHistory:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        state_ids = self._storage.load_state_ids(chat_id=chat_id, user_id=user_id)

        return StateHistory(state_ids)

    def get_flow_state_history(
        self,
        flow_id: int
    ) -> StateHistory:
        state_ids = self._storage.load_flow_state_ids(flow_id=flow_id)

        return StateHistory(state_ids)

    def get_current_state_history(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT
    ) -> StateHistory:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        state_ids = self._storage.load_current_state_ids(chat_id=chat_id, user_id=user_id)

        return StateHistory(state_ids)

    def switch_state(
        self,
        state_id: int,
        *,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        history = self.get_state_history(chat_id=ctx.chat_id, user_id=ctx.user_id)
        self._process_transition(history=history, state_id=state_id, ctx=ctx)

    def revert_state(
        self,
        *,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        history = self.get_state_history(chat_id=ctx.chat_id, user_id=ctx.user_id)

        if history.previous_state_id is None:
            raise PreviousStateNotFoundError(
                f"State history has no previous state for chat_id={ctx.chat_id}, user_id={ctx.user_id}!"
            )

        self._process_transition(history=history, state_id=history.previous_state_id, ctx=ctx)

    def reenter_state(
        self,
        *,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        history = self.get_state_history(chat_id=ctx.chat_id, user_id=ctx.user_id)
        self._process_transition(history=history, state_id=history.state_id, ctx=ctx)

    def switch_flow_state(
        self,
        state_id: int,
        *,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        history = self.get_flow_state_history(flow_id=ctx.flow.id)
        self._process_flow_transition(history=history, state_id=state_id, ctx=ctx)

    def revert_flow_state(
        self,
        *,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        history = self.get_flow_state_history(flow_id=ctx.flow.id)

        if history.previous_state_id is None:
            raise PreviousStateNotFoundError(
                f"Flow state history has no previous state for flow_id={ctx.flow.id}!"
            )

        self._process_flow_transition(history=history, state_id=history.previous_state_id, ctx=ctx)

    def reenter_flow_state(
        self,
        *,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        history = self.get_flow_state_history(flow_id=ctx.flow.id)
        self._process_flow_transition(history=history, state_id=history.state_id, ctx=ctx)

    def get_input_flow_id(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT
    ) -> Optional[int]:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)

        return self._storage.load_input_flow_id(chat_id=chat_id, user_id=user_id)

    def _process_transition(
        self,
        history: StateHistory,
        state_id: int,
        *,
        ctx: "EventContext"
    ) -> None:
        if state_id != history.state_id:
            for hook in self._state_exit_hooks.get(history.state_id, ()):
                hook(ctx)

            history.set_state_id(state_id)

        self._storage.save_state_transition(
            state_ids=history.state_ids,
            chat_id=ctx.chat_id,
            user_id=ctx.user_id
        )

        for hook in self._state_enter_hooks.get(state_id, ()):
            hook(ctx)

    def _process_flow_transition(
        self,
        history: StateHistory,
        state_id: int,
        *,
        ctx: "EventContext"
    ) -> None:
        if state_id != history.state_id:
            for hook in self._flow_state_exit_hooks.get(history.state_id, ()):
                hook(ctx)

            history.set_state_id(state_id)

        self._storage.save_flow_state_transition(
            state_ids=history.state_ids,
            flow_id=ctx.flow.id,
            chat_id=ctx.chat_id,
            user_id=ctx.user_id,
            input_flow_id=ctx.flow.id if state_id in self._input_flow_state_ids else None
        )

        for hook in self._flow_state_enter_hooks.get(state_id, ()):
            hook(ctx)


def _get_ctx(ctx: Union["EventContext", FromContext]) -> "EventContext":
    if isinstance(ctx, FromContext):
        return event_context_context.get()

    return ctx


def _get_chat_id(chat_id: Union[int, FromContext]) -> int:
    if isinstance(chat_id, FromContext):
        return chat_id_context.get()

    return chat_id


def _get_user_id(user_id: Union[int, None, FromContext]) -> int:
    if isinstance(user_id, FromContext):
        return user_id_context.get(None)

    return user_id
