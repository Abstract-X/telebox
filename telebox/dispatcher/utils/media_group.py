from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

from telebox.bot.types.types.message import Message
from telebox.bot.types.types.user import User
from telebox.bot.types.types.chat import Chat
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


@dataclass
class MediaGroup:
    messages: list[Message]

    def __post_init__(self):
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
        return self.messages[0].caption

    @property
    def caption_entities(self) -> Optional[list[MessageEntity]]:
        return self.messages[0].caption_entities

    @property
    def sender_chat(self) -> Optional[Chat]:
        return self.messages[0].sender_chat

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
