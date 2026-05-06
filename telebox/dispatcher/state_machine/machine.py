from typing import Optional, Union, Callable, TYPE_CHECKING
from dataclasses import dataclass

from telebox.dispatcher.state_machine.errors import PreviousStateNotFoundError
from telebox.dispatcher.state_machine.storage import AbstractStateBundleStorage
from telebox.context_values import (
    event_context_context,
    chat_id_context,
    user_id_context,
    FromContext,
    FROM_CONTEXT,
    OPTIONAL_FROM_CONTEXT
)
if TYPE_CHECKING:
    from telebox.dispatcher.context import EventContext


@dataclass
class StateBundle:
    magazine: list[str]
    flow_id: Optional[int] = None

    @property
    def state(self) -> str:
        return self.magazine[-1]

    @property
    def previous_state(self) -> Optional[str]:
        return self.magazine[-2] if len(self.magazine) > 1 else None


class StateMachine:
    def __init__(self, initial_state: str, storage: AbstractStateBundleStorage):
        self._initial_state = initial_state
        self._storage = storage
        self._enter_hooks: dict[str, list[Callable[["EventContext"], None]]] = {}
        self._exit_hooks: dict[str, list[Callable[["EventContext"], None]]] = {}

    @property
    def initial_state(self) -> str:
        return self._initial_state

    def add_enter_hook(self, state: str, hook: Callable[["EventContext"], None]) -> None:
        self._enter_hooks.setdefault(state, []).append(hook)

    def add_exit_hook(self, state: str, hook: Callable[["EventContext"], None]) -> None:
        self._exit_hooks.setdefault(state, []).append(hook)

    def get_bundle(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT
    ) -> StateBundle:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        magazine, flow_id = self._storage.load(chat_id=chat_id, user_id=user_id)

        if not magazine:
            magazine = [self.initial_state]

        return StateBundle(magazine=magazine, flow_id=flow_id)

    def set_state(
        self,
        state: str,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT,
        flow_id: Optional[int] = None
    ) -> None:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        bundle = self.get_bundle(chat_id=chat_id, user_id=user_id)
        _set_magazine_state(magazine=bundle.magazine, state=state)
        self._update_bundle(
            magazine=bundle.magazine,
            chat_id=chat_id,
            user_id=user_id,
            flow_id=flow_id
        )

    def set_previous_state(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT,
        flow_id: Optional[int] = None
    ) -> None:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        bundle = self.get_bundle(chat_id=chat_id, user_id=user_id)

        if bundle.previous_state is None:
            raise PreviousStateNotFoundError(
                f"No previous state for chat_id={chat_id}, user_id={user_id}!"
            )

        _set_magazine_state(magazine=bundle.magazine, state=bundle.previous_state)
        self._update_bundle(
            magazine=bundle.magazine,
            chat_id=chat_id,
            user_id=user_id,
            flow_id=flow_id
        )

    def switch_state(
        self,
        state: str,
        *,
        flow_id: Optional[int] = None,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        bundle = self.get_bundle(chat_id=ctx.chat_id, user_id=ctx.user_id)
        self._process_transition(
            bundle=bundle,
            state=state,
            ctx=ctx,
            flow_id=flow_id
        )

    def revert_state(
        self,
        *,
        flow_id: Optional[int] = None,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        bundle = self.get_bundle(chat_id=ctx.chat_id, user_id=ctx.user_id)

        if bundle.previous_state is None:
            raise PreviousStateNotFoundError(
                f"No previous state for chat_id={ctx.chat_id}, user_id={ctx.user_id}!"
            )

        self._process_transition(
            bundle=bundle,
            state=bundle.previous_state,
            ctx=ctx,
            flow_id=flow_id
        )

    def _update_bundle(
        self,
        magazine: list[str],
        *,
        chat_id: int,
        user_id: Optional[int] = None,
        flow_id: Optional[int] = None
    ) -> None:
        self._storage.save(
            magazine=magazine,
            chat_id=chat_id,
            user_id=user_id,
            flow_id=flow_id
        )

    def _process_transition(
        self,
        bundle: StateBundle,
        state: str,
        ctx: "EventContext",
        flow_id: Optional[int] = None
    ) -> None:
        if state != bundle.state:
            for hook in self._exit_hooks.get(bundle.state, ()):
                hook(ctx)

            _set_magazine_state(magazine=bundle.magazine, state=state)
            self._update_bundle(
                magazine=bundle.magazine,
                chat_id=ctx.chat_id,
                user_id=ctx.user_id,
                flow_id=flow_id
            )

        for hook in self._enter_hooks.get(state, ()):
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


def _set_magazine_state(magazine: list[str], state: str) -> None:
    try:
        index = magazine.index(state)
    except ValueError:
        magazine.append(state)
    else:
        del magazine[index + 1:]
