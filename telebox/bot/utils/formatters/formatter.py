from abc import ABC, abstractmethod
from typing import Optional

from telebox.bot.utils.deep_links import get_user_link
from telebox.bot.types.types.message_entity import MessageEntity
from telebox.bot.consts import message_entity_types
from telebox.utils.text import get_text_with_surrogates, get_text_without_surrogates


_FORMATTING_ENTITY_TYPES = {
    message_entity_types.BOLD,
    message_entity_types.ITALIC,
    message_entity_types.UNDERLINE,
    message_entity_types.STRIKETHROUGH,
    message_entity_types.SPOILER,
    message_entity_types.TEXT_LINK,
    message_entity_types.CODE,
    message_entity_types.PRE,
    message_entity_types.TEXT_MENTION
}


class AbstractFormatter(ABC):

    @abstractmethod
    def get_escaped_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_bold_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_italic_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_underline_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_strikethrough_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_spoiler_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_text_link_text(self, text: str, link: str) -> str:
        pass

    @abstractmethod
    def get_code_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_pre_text(self, text: str, language: Optional[str] = None) -> str:
        pass

    def get_text_mention_text(self, text: str, user_id: int) -> str:
        return self.get_text_link_text(
            text=text,
            link=get_user_link(user_id)
        )

    def get_formatted_text(self, text: str, entities: list[MessageEntity]) -> str:
        text = get_text_with_surrogates(text)
        entities = [i for i in entities if i.type in _FORMATTING_ENTITY_TYPES]
        entities.sort(key=lambda entity: entity.offset)

        return self._get_formatted_text(
            text=text,
            entities=entities,
            offset=0,
            length=len(text)
        )

    def _get_formatted_text(
        self,
        text: bytes,
        entities: list[MessageEntity],
        offset: int,
        length: int
    ) -> str:
        formatted_text = ""

        for index, entity in enumerate(entities):
            entity_offset = entity.offset * 2

            if entity_offset < offset:
                continue
            else:
                formatted_text += self.get_escaped_text(
                    get_text_without_surrogates(text[offset:entity_offset])
                )

            offset = entity.end_offset * 2
            nested_entities = [i for i in entities[index + 1:] if i.offset * 2 < offset]
            entity_text = self._get_formatted_text(
                text=text,
                entities=nested_entities,
                offset=entity_offset,
                length=offset
            )

            if entity.type == message_entity_types.BOLD:
                formatted_text += self.get_bold_text(entity_text)
            elif entity.type == message_entity_types.ITALIC:
                formatted_text += self.get_italic_text(entity_text)
            elif entity.type == message_entity_types.UNDERLINE:
                formatted_text += self.get_underline_text(entity_text)
            elif entity.type == message_entity_types.STRIKETHROUGH:
                formatted_text += self.get_strikethrough_text(entity_text)
            elif entity.type == message_entity_types.SPOILER:
                formatted_text += self.get_spoiler_text(entity_text)
            elif entity.type == message_entity_types.TEXT_LINK:
                formatted_text += self.get_text_link_text(entity_text, entity.url)
            elif entity.type == message_entity_types.CODE:
                formatted_text += self.get_code_text(entity_text)
            elif entity.type == message_entity_types.PRE:
                formatted_text += self.get_pre_text(entity_text, entity.language)
            elif entity.type == message_entity_types.TEXT_MENTION:
                formatted_text += self.get_text_mention_text(entity_text, entity.user.id)

        if offset < length:
            formatted_text += self.get_escaped_text(
                get_text_without_surrogates(
                    text[offset:length]
                )
            )

        return formatted_text
