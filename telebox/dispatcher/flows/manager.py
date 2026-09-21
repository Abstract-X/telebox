from typing import Optional, Union, overload, Callable, TypeVar
import functools

from telebox.bot.types.callback_query import CallbackQuery
from telebox.dispatcher.flows.storage import AbstractFlowStorage
from telebox.dispatcher.flows.flow import Flow
from telebox.dispatcher.flows.errors import FlowNotFoundError, FlowAlreadyExistsError
from telebox.context_values import (
    FromContext,
    FROM_CONTEXT,
    OPTIONAL_FROM_CONTEXT,
    chat_id_context,
    user_id_context
)


F = TypeVar("F", bound=Callable)


@overload
def with_flow(func: F, *, start: bool = False, chat: bool = False) -> F: ...


@overload
def with_flow(*, start: bool = False, chat: bool = False) -> Callable[[F], F]: ...


def with_flow(func=None, /, *, start: bool = False, chat: bool = False):
    def decorator(callback: F) -> F:
        @functools.wraps(callback)
        def wrapper(ctx):
            if ctx.flow is not None:
                return callback(ctx)

            chat_id = ctx.chat_id
            user_id = None if chat else ctx.user_id

            if isinstance(ctx.event, CallbackQuery):
                flow_id = ctx.event.flow_id
            else:
                flow_id = ctx.state_machine.get_input_flow_id(chat_id=chat_id, user_id=user_id)

            if start:
                if flow_id is not None:
                    raise FlowAlreadyExistsError(
                        f"Cannot start a new flow: flow_id={flow_id} already exists "
                        f"for chat_id={chat_id}, user_id={user_id}!"
                    )

                flow_id = ctx.flow_manager.start_flow(chat_id=chat_id, user_id=user_id)
            elif flow_id is None:
                raise FlowNotFoundError(f"Flow not found for chat_id={chat_id}, user_id={user_id}!")

            with ctx.flow_manager.flow(flow_id) as flow:
                ctx.flow = flow

                return callback(ctx)

        return wrapper

    if func is None:
        return decorator

    return decorator(func)


class FlowContext:
    def __init__(self, flow_id: int, storage: AbstractFlowStorage):
        self._flow_id = flow_id
        self._storage = storage
        self.flow: Optional[Flow] = None

    def __enter__(self) -> Flow:
        self.flow = Flow(
            id_=self._flow_id,
            data=self._storage.load(
                flow_id=self._flow_id
            )
        )

        return self.flow

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (exc_type is None) and (self.flow is not None) and self.flow.is_changed:
            self._storage.save(flow_id=self.flow.id, data=self.flow.data)


class FlowManager:
    def __init__(self, storage: AbstractFlowStorage) -> None:
        self._storage = storage

    def start_flow(
        self,
        *,
        chat_id: Union[int, FromContext] = FROM_CONTEXT,
        user_id: Union[int, None, FromContext] = OPTIONAL_FROM_CONTEXT
    ) -> int:
        chat_id = _get_chat_id(chat_id)
        user_id = _get_user_id(user_id)

        return self._storage.create(chat_id=chat_id, user_id=user_id)

    def get_flow(self, flow_id: int) -> Flow:
        return Flow(
            id_=flow_id,
            data=self._storage.load(
                flow_id=flow_id
            )
        )

    def flow(self, flow_id: int) -> FlowContext:
        return FlowContext(flow_id=flow_id, storage=self._storage)

    def save_flow(self, flow: Flow) -> None:
        self._storage.save(flow_id=flow.id, data=flow.data)

    def finish_flow(self, flow_id: int) -> None:
        self._storage.finish(flow_id)


def _get_chat_id(chat_id: Union[int, FromContext]) -> int:
    if isinstance(chat_id, FromContext):
        return chat_id_context.get()

    return chat_id


def _get_user_id(user_id: Union[int, None, FromContext]) -> int:
    if isinstance(user_id, FromContext):
        return user_id_context.get(None)

    return user_id
