from typing import Union

from telebox.dispatcher.filters.events.filter import AbstractEventFilter
from telebox.dispatcher.enums.event_type import EventType
from telebox.dispatcher.utils.media_group import MediaGroup
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.inline_query import InlineQuery
from telebox.bot.types.types.chosen_inline_result import ChosenInlineResult
from telebox.bot.types.types.callback_query import CallbackQuery
from telebox.bot.types.types.shipping_query import ShippingQuery
from telebox.bot.types.types.pre_checkout_query import PreCheckoutQuery
from telebox.bot.types.types.poll_answer import PollAnswer
from telebox.bot.types.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.types.chat_join_request import ChatJoinRequest


class UserFilter(AbstractEventFilter):

    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_event_types(self) -> set[EventType]:
        return {
            EventType.MESSAGE,
            EventType.EDITED_MESSAGE,
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

    def check_event(
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
                     ChatJoinRequest]
    ) -> bool:
        user_id = event.user_id

        if self._ids:
            return user_id in self._ids

        return user_id is not None
