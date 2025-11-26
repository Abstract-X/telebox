from typing import Union, Optional

from telebox.dispatcher.filter import AbstractFilter
from telebox.dispatcher.types.media_group import MediaGroup
from telebox.bot.types.message import Message
from telebox.bot.types.callback_query import CallbackQuery
from telebox.bot.types.chat_member_updated import ChatMemberUpdated
from telebox.bot.types.chat_join_request import ChatJoinRequest
from telebox.bot.types.business_messages_deleted import BusinessMessagesDeleted
from telebox.bot.types.chat_boost_removed import ChatBoostRemoved
from telebox.bot.types.chat_boost_updated import ChatBoostUpdated
from telebox.bot.types.message_reaction_count_updated import MessageReactionCountUpdated
from telebox.bot.types.message_reaction_updated import MessageReactionUpdated
from telebox.bot.types.poll_answer import PollAnswer


class ChatFilter(AbstractFilter):
    def __init__(self, *ids: int):
        self._ids = set(ids)

    def get_value(
        self,
        event: Union[
            Message,
            MediaGroup,
            CallbackQuery,
            ChatMemberUpdated,
            ChatJoinRequest,
            BusinessMessagesDeleted,
            ChatBoostRemoved,
            ChatBoostUpdated,
            MessageReactionCountUpdated,
            MessageReactionUpdated,
            PollAnswer
        ]
    ) -> Optional[int]:
        return event.chat_id

    def check_value(self, value: Optional[int]) -> bool:
        if self._ids:
            return value in self._ids

        return value is not None
