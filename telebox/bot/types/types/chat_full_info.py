from dataclasses import dataclass
from typing import Literal, Optional
from datetime import datetime

from telebox.bot.types.type import Type
from telebox.bot.utils.users import get_full_name
from telebox.bot.utils.deep_links import get_username_link
from telebox.bot.types.types.chat_photo import ChatPhoto
from telebox.bot.types.types.chat_permissions import ChatPermissions
from telebox.bot.types.types.chat_location import ChatLocation
from telebox.bot.types.types.reaction_type import ReactionType
from telebox.bot.types.types.birthdate import Birthdate
from telebox.bot.types.types.business_intro import BusinessIntro
from telebox.bot.types.types.business_location import BusinessLocation
from telebox.bot.types.types.business_opening_hours import BusinessOpeningHours
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.message import Message


@dataclass(repr=False)
class ChatFullInfo(Type):
    id: int
    type: str
    accent_color_id: int
    max_reaction_count: int
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[Literal[True]] = None
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[list[str]] = None
    birthdate: Optional[Birthdate] = None
    business_intro: Optional[BusinessIntro] = None
    business_location: Optional[BusinessLocation] = None
    business_opening_hours: Optional[BusinessOpeningHours] = None
    personal_chat: Optional[Chat] = None
    available_reactions: Optional[list[ReactionType]] = None
    background_custom_emoji_id: Optional[str] = None
    profile_accent_color_id: Optional[int] = None
    profile_background_custom_emoji_id: Optional[str] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    emoji_status_expiration_date: Optional[datetime] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[Literal[True]] = None
    has_restricted_voice_and_video_messages: Optional[Literal[True]] = None
    join_to_send_messages: Optional[Literal[True]] = None
    join_by_request: Optional[Literal[True]] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional[Message] = None
    permissions: Optional[ChatPermissions] = None
    can_send_paid_media: Optional[Literal[True]] = None
    slow_mode_delay: Optional[int] = None
    unrestrict_boost_count: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_aggressive_anti_spam_enabled: Optional[Literal[True]] = None
    has_hidden_members: Optional[Literal[True]] = None
    has_protected_content: Optional[Literal[True]] = None
    has_visible_history: Optional[Literal[True]] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[Literal[True]] = None
    custom_emoji_sticker_set_name: Optional[str] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None

    @property
    def full_name(self) -> Optional[str]:
        if self.first_name is not None:
            return get_full_name(self.first_name, self.last_name)

    @property
    def link(self) -> Optional[str]:
        if self.username is not None:
            return get_username_link(self.username)
        elif self.invite_link is not None:
            return self.invite_link
