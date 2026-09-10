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
    magazine: list[int]
    flow_id: Optional[int] = None

    @property
    def state_id(self) -> int:
        return self.magazine[-1]

    @property
    def previous_state_id(self) -> Optional[int]:
        return self.magazine[-2] if len(self.magazine) > 1 else None


class StateMachine:
    def __init__(self, initial_state_id: str, storage: AbstractStateBundleStorage):
        self._initial_state_id = initial_state_id
        self._storage = storage
        self._enter_hooks: dict[int, list[Callable[["EventContext"], None]]] = {}
        self._exit_hooks: dict[int, list[Callable[["EventContext"], None]]] = {}

    @property
    def initial_state(self) -> str:
        return self._initial_state_id

    def add_enter_hook(self, state_id: int, hook: Callable[["EventContext"], None]) -> None:
        self._enter_hooks.setdefault(state_id, []).append(hook)

    def add_exit_hook(self, state_id: int, hook: Callable[["EventContext"], None]) -> None:
        self._exit_hooks.setdefault(state_id, []).append(hook)

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

    def set_state_id(
        self,
        state_id: int,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT,
        flow_id: Optional[int] = None
    ) -> None:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        bundle = self.get_bundle(chat_id=chat_id, user_id=user_id)
        _set_magazine_state(magazine=bundle.magazine, state_id=state_id)
        self._update_bundle(
            magazine=bundle.magazine,
            chat_id=chat_id,
            user_id=user_id,
            flow_id=flow_id
        )

    def set_previous_state_id(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT,
        flow_id: Optional[int] = None
    ) -> None:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)
        bundle = self.get_bundle(chat_id=chat_id, user_id=user_id)

        if bundle.previous_state_id is None:
            raise PreviousStateNotFoundError(
                f"No previous state for chat_id={chat_id}, user_id={user_id}!"
            )

        _set_magazine_state(magazine=bundle.magazine, state_id=bundle.previous_state_id)
        self._update_bundle(
            magazine=bundle.magazine,
            chat_id=chat_id,
            user_id=user_id,
            flow_id=flow_id
        )

    def switch_state(
        self,
        state_id: int,
        *,
        flow_id: Optional[int] = None,
        ctx: Union["EventContext", FromContext] = FROM_CONTEXT
    ) -> None:
        ctx = _get_ctx(ctx)
        bundle = self.get_bundle(chat_id=ctx.chat_id, user_id=ctx.user_id)
        self._process_transition(
            bundle=bundle,
            state_id=state_id,
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

        if bundle.previous_state_id is None:
            raise PreviousStateNotFoundError(
                f"No previous state for chat_id={ctx.chat_id}, user_id={ctx.user_id}!"
            )

        self._process_transition(
            bundle=bundle,
            state_id=bundle.previous_state_id,
            ctx=ctx,
            flow_id=flow_id
        )

    def _update_bundle(
        self,
        magazine: list[int],
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
        state_id: int,
        ctx: "EventContext",
        flow_id: Optional[int] = None
    ) -> None:
        if state_id != bundle.state_id:
            for hook in self._exit_hooks.get(bundle.state_id, ()):
                hook(ctx)

            _set_magazine_state(magazine=bundle.magazine, state_id=state_id)
            self._update_bundle(
                magazine=bundle.magazine,
                chat_id=ctx.chat_id,
                user_id=ctx.user_id,
                flow_id=flow_id
            )

        for hook in self._enter_hooks.get(state_id, ()):
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


def _set_magazine_state(magazine: list[int], state_id: int) -> None:
    try:
        index = magazine.index(state_id)
    except ValueError:
        magazine.append(state_id)
    else:
        del magazine[index + 1:]
