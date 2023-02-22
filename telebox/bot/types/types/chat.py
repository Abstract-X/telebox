from dataclasses import dataclass
from typing import Literal, Optional, TYPE_CHECKING

from telebox.bot.types.type import Type
from telebox.bot.utils.users import get_full_name
from telebox.bot.utils.deep_links import get_username_link
from telebox.bot.types.types.chat_photo import ChatPhoto
from telebox.bot.types.types.chat_permissions import ChatPermissions
from telebox.bot.types.types.chat_location import ChatLocation
if TYPE_CHECKING:
    from telebox.bot.types.types.message import Message


@dataclass
class Chat(Type):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_forum: Optional[Literal[True]] = None
    photo: Optional[ChatPhoto] = None
    active_usernames: Optional[list[str]] = None
    emoji_status_custom_emoji_id: Optional[str] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[Literal[True]] = None
    has_restricted_voice_and_video_messages: Optional[Literal[True]] = None
    join_to_send_messages: Optional[Literal[True]] = None
    join_by_request: Optional[Literal[True]] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional["Message"] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[Literal[True]] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[Literal[True]] = None
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
