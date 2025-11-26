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


class ChatTypeFilter(AbstractFilter):
    def __init__(self, *types: str):
        if not types:
            raise ValueError("No chat types!")

        self._types = set(types)

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
    ) -> Optional[str]:
        return event.chat_type

    def check_value(self, value: Optional[str]) -> bool:
        return value in self._types
