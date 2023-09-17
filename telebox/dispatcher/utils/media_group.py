from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

from telebox.bot.types.types.message import Message
from telebox.bot.types.types.user import User
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.utils.ids import get_unprefixed_chat_id
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


@dataclass
class MediaGroup:
    messages: list[Message]

    def __post_init__(self):
        self.messages.sort(key=lambda message: message.message_id)
        self._content_types = set()

        for i in self.messages:
            self._content_types.add(
                MediaGroupContentType(i.content_type.value)
            )

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
    def message_thread_id(self) -> Optional[int]:
        return self.messages[0].message_thread_id

    @property
    def message_topic_id(self) -> Optional[int]:
        return self.messages[0].message_topic_id

    @property
    def from_(self) -> Optional[User]:
        return self.messages[0].from_

    @property
    def caption(self) -> Optional[str]:
        for i in self.messages:
            if i.caption is not None:
                return i.caption

    @property
    def caption_entities(self) -> Optional[list[MessageEntity]]:
        for i in self.messages:
            if i.caption_entities:
                return i.caption_entities

    @property
    def sender_chat(self) -> Optional[Chat]:
        return self.messages[0].sender_chat

    @property
    def sender_chat_id(self) -> Optional[int]:
        return self.messages[0].sender_chat_id

    @property
    def forward_from(self) -> Optional[User]:
        return self.messages[0].forward_from

    @property
    def forward_from_chat(self) -> Optional[Chat]:
        return self.messages[0].forward_from_chat

    @property
    def forward_signature(self) -> Optional[str]:
        return self.messages[0].forward_signature

    @property
    def forward_sender_name(self) -> Optional[str]:
        return self.messages[0].forward_sender_name

    @property
    def forward_date(self) -> Optional[datetime]:
        return self.messages[0].forward_date

    @property
    def is_topic_messages(self) -> Optional[Literal[True]]:
        return self.messages[0].is_topic_message

    @property
    def is_automatic_forward(self) -> Optional[Literal[True]]:
        return self.messages[0].is_automatic_forward

    @property
    def reply_to_message(self) -> Optional[Message]:
        return self.messages[0].reply_to_message

    @property
    def has_protected_content(self) -> Optional[Literal[True]]:
        return self.messages[0].has_protected_content

    @property
    def author_signature(self) -> Optional[str]:
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
        return get_unprefixed_chat_id(self.chat_id, self.chat_type)

    @property
    def sender_chat_id(self) -> Optional[int]:
        return self.messages[0].sender_chat_id

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
    def link(self) -> str:
        return self.messages[0].link

    def get_text(self) -> Optional[str]:
        for i in self.messages:
            text = i.get_text()

            if text:
                return text

    def get_html_text(self) -> Optional[str]:
        for i in self.messages:
            text = i.get_html_text()

            if text:
                return text

    def get_markdown_text(self) -> Optional[str]:
        for i in self.messages:
            text = i.get_markdown_text()

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

    def get_command_args(self) -> list[str]:
        for i in self.messages:
            text = i.get_text()

            if text:
                return i.get_command_args()

        return []
