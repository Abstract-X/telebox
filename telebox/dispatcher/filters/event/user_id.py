from typing import Optional, Union

from telebox.dispatcher.filters.event_filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.media_group import MediaGroup
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
        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
            EventType.CHANNEL_POST,
            EventType.EDITED_CHANNEL_POST,
            EventType.MEDIA_GROUP,
            EventType.INLINE_QUERY,
            EventType.CHOSEN_INLINE_RESULT,
            EventType.CALLBACK_QUERY,
            EventType.SHIPPING_QUERY,
            EventType.PRE_CHECKOUT_QUERY,
            EventType.POLL_ANSWER,
            EventType.MY_CHAT_MEMBER,
            EventType.CHAT_MEMBER,
            EventType.CHAT_JOIN_REQUEST
        }

    def get_value(
        self,
        event: Union[Message,
                     MediaGroup,
                     InlineQuery,
                     ChosenInlineResult,
                     CallbackQuery,
                     ShippingQuery,
                     PreCheckoutQuery,
                     PollAnswer,
                     ChatMemberUpdated,
                     ChatJoinRequest],
        event_type: EventType
    ) -> Optional[int]:
        return event.user_id

    def check_value(self, value: Optional[int]) -> bool:
        return value in self._ids if self._ids else value is not None
