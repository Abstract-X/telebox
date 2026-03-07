from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal, Union

from telebox.bot.types.message import Message
from telebox.bot.types.user import User
from telebox.bot.types.chat import Chat
from telebox.bot.types.message_origin import MessageOrigin
from telebox.bot.types.message_entity import MessageEntity
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType
from telebox.unset import Unset


@dataclass
class MediaGroup:
    messages: list[Message]

    def __post_init__(self):
        self.messages.sort(key=lambda message: message.message_id)
        self._content_types = {MediaGroupContentType(i.type.value) for i in self.messages}

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, item):
        return self.messages.__getitem__(item)

    @property
    def id(self) -> str:
        return self.messages[0].media_group_id

    @property
    def chat(self) -> Chat:
        return self.messages[0].chat

    @property
    def message_id(self) -> int:
        return self.messages[0].message_id

    @property
    def message_thread_id(self) -> Union[int, None, Unset]:
        return self.messages[0].message_thread_id

    @property
    def from_(self) -> Union[User, None, Unset]:
        return self.messages[0].from_

    @property
    def caption(self) -> Optional[str]:
        for i in self.messages:
            if i.caption:
                return i.caption

    @property
    def caption_entities(self) -> list[MessageEntity]:
        for i in self.messages:
            if i.caption_entities:
                return i.caption_entities

        return []

    @property
    def sender_chat(self) -> Union[Chat, None, Unset]:
        return self.messages[0].sender_chat

    @property
    def sender_chat_id(self) -> Union[int, None, Unset]:
        return self.messages[0].sender_chat_id

    @property
    def forward_origin(self) -> Union[MessageOrigin, None, Unset]:
        return self.messages[0].forward_origin

    @property
    def business_connection_id(self) -> Union[str, None, Unset]:
        return self.messages[0].business_connection_id

    @property
    def is_automatic_forward(self) -> Union[Literal[True], None, Unset]:
        return self.messages[0].is_automatic_forward

    @property
    def reply_to_message(self) -> Union[Message, None, Unset]:
        return self.messages[0].reply_to_message

    @property
    def has_protected_content(self) -> Union[Literal[True], None, Unset]:
        return self.messages[0].has_protected_content

    @property
    def author_signature(self) -> Union[str, None, Unset]:
        return self.messages[0].author_signature

    @property
    def content_types(self) -> set[MediaGroupContentType]:
        return self._content_types

    @property
    def date(self) -> datetime:
        return self.messages[0].date

    @property
    def chat_type(self) -> str:
        return self.messages[0].chat_type

    @property
    def chat_id(self) -> int:
        return self.messages[0].chat_id

    @property
    def unprefixed_chat_id(self) -> int:
        return self.messages[0].unprefixed_chat_id

    @property
    def unprefixed_sender_chat_id(self) -> Optional[int]:
        return self.messages[0].unprefixed_sender_chat_id

    @property
    def user_id(self) -> Optional[int]:
        return self.messages[0].user_id

    @property
    def is_forwarded(self) -> bool:
        return self.messages[0].is_forwarded

    @property
    def is_reply(self) -> bool:
        return self.messages[0].is_reply

    @property
    def link(self) -> Optional[str]:
        return self.messages[0].link

    def get_text(self, parse_mode: Optional[str] = None) -> Optional[str]:
        for i in self.messages:
            text = i.get_text(parse_mode)

            if text:
                return text

    def get_entity_text(self, entity: MessageEntity) -> Optional[str]:
        for i in self.messages:
            entities = i.get_entities()

            if entities:
                return i.get_entity_text(entity)

    def get_entities(self) -> list[MessageEntity]:
        for i in self.messages:
            entities = i.get_entities()

            if entities:
                return entities

        return []

    def get_command_args(self) -> list[str]:
        for i in self.messages:
            text = i.get_text()

            if text:
                return i.get_command_args()

        return []
