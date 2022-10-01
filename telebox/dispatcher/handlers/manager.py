from typing import Union, Optional, Literal

from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler
from telebox.dispatcher.handlers.handlers.error import AbstractErrorHandler
from telebox.dispatcher.handlers.filters.base.base import (
    AbstractFilter,
    ExpressionType,
    AbstractExpression,
    NoneExpression,
    FilterExpression,
    InvertExpression,
    AndExpression,
    OrExpression
)
from telebox.dispatcher.handlers.filters.base.event import AbstractEventFilter
from telebox.dispatcher.handlers.filters.base.error import AbstractErrorFilter
from telebox.typing import Event


EventHandlerDict = dict[
    EventType,
    list[
        tuple[
            AbstractEventHandler,
            AbstractExpression
        ]
    ]
]
ErrorHandlerList = list[
    tuple[
        AbstractErrorHandler,
        AbstractExpression
    ]
]
EventFilter = Union[AbstractEventFilter, AbstractExpression, None]
ErrorFilter = Union[AbstractErrorFilter, AbstractExpression, None]


class HandlerManager:

    def __init__(self):
        self._event_handlers: EventHandlerDict = {i: [] for i in EventType}
        self._error_handlers: ErrorHandlerList = []

    def add_event_handler(
        self,
        handler: AbstractEventHandler,
        event_type: EventType,
        filter_: Optional[EventFilter] = None
    ) -> None:
        self._event_handlers[event_type].append((handler, _get_expression(filter_)))

    def add_error_handler(
        self,
        handler: AbstractErrorHandler,
        filter_: Optional[ErrorFilter] = None
    ) -> None:
        self._error_handlers.append((handler, _get_expression(filter_)))

    def get_event_handler(
        self,
        event: Event,
        event_type: EventType
    ) -> Optional[AbstractEventHandler]:
        return _get_handler(self._event_handlers[event_type], (event,))

    def get_error_handler(
        self,
        error: Exception,
        event: Event
    ) -> Optional[AbstractErrorHandler]:
        return _get_handler(self._error_handlers, (error, event))


def _get_handler(handlers: list[tuple], value_getting_args: tuple):
    filter_values = {}

    for handler, filter_ in handlers:
        result_getter = _EXPRESSION_RESULT_GETTERS[filter_.get_type()]

        if result_getter(filter_, filter_values, value_getting_args):
            return handler


# noinspection PyUnusedLocal
def _get_none_expression_result(
    expression: NoneExpression,
    values: dict,
    value_getting_args: tuple
) -> Literal[True]:
    return True


def _get_filter_expression_result(
    expression: FilterExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    filter_ = expression.value
    filter_type = type(filter_)

    try:
        value = values[filter_type]
    except KeyError:
        value = values[filter_type] = filter_.get_value(*value_getting_args)

    return filter_.check_value(value)


def _get_invert_expression_result(
    expression: InvertExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    result_getter = _EXPRESSION_RESULT_GETTERS[expression.value.get_type()]

    return not result_getter(expression.value, values, value_getting_args)


def _get_and_expression_result(
    expression: AndExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    return all(
        _EXPRESSION_RESULT_GETTERS[i.get_type()](i, values, value_getting_args)
        for i in expression
    )


def _get_or_expression_result(
    expression: OrExpression,
    values: dict,
    value_getting_args: tuple
) -> bool:
    return any(
        _EXPRESSION_RESULT_GETTERS[i.get_type()](i, values, value_getting_args)
        for i in expression
    )


_EXPRESSION_RESULT_GETTERS = {
    ExpressionType.NONE: _get_none_expression_result,
    ExpressionType.FILTER: _get_filter_expression_result,
    ExpressionType.INVERT: _get_invert_expression_result,
    ExpressionType.AND: _get_and_expression_result,
    ExpressionType.OR: _get_or_expression_result
}


def _get_expression(filter_) -> AbstractExpression:
    if filter_ is None:
        return NoneExpression()
    elif isinstance(filter_, AbstractFilter):
        return FilterExpression(filter_)
    elif isinstance(filter_, AbstractExpression):
        return filter_

    raise ValueError(f"Unknown filter type {filter_!r}!")
