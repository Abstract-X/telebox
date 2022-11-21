from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from telebox.bot.types.types.message import Message
from telebox.dispatcher.enums.media_group_content_type import MediaGroupContentType


@dataclass(unsafe_hash=True)
class MediaGroup:
    messages: list[Message]

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
    def message_thread_id(self) -> Optional[int]:
        return self.messages[0].message_thread_id

    @property
    def content_types(self) -> set[MediaGroupContentType]:
        content_types = set()

        for i in self.messages:
            _, content_type = i.content
            content_type = MediaGroupContentType(content_type.value)
            content_types.add(content_type)

        return content_types

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
