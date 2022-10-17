from typing import Optional

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.dispatcher import Event
from telebox.dispatcher.enums.event_type import EventType
from telebox.telegram_bot.types.types.message import Message
from telebox.telegram_bot.types.types.inline_query import InlineQuery
from telebox.telegram_bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.telegram_bot.types.types.callback_query import CallbackQuery
from telebox.telegram_bot.types.types.shipping_query import ShippingQuery
from telebox.telegram_bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.telegram_bot.types.types.poll_answer import PollAnswer
from telebox.telegram_bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.telegram_bot.types.types.chat_join_request import ChatJoinRequest


class UserIDFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        if not ids:
            raise ValueError("No user identifiers!")

        self._ids = set(ids)

    def get_value(self, event: Event, event_type: EventType) -> Optional[int]:
        if isinstance(
            event,
            (
                Message,
                InlineQuery,
                ChosenInlineResult,
                CallbackQuery,
                ShippingQuery,
                PreCheckoutQuery,
                PollAnswer,
                ChatMemberUpdated,
                ChatJoinRequest
            )
        ):
            return event.user_id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids
