from abc import ABC, abstractmethod
from typing import Optional
import re

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
    message_entity_types.TEXT_MENTION,
    message_entity_types.BLOCKQUOTE,
    message_entity_types.EXPANDABLE_BLOCKQUOTE
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

    @abstractmethod
    def get_blockquote_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_expandable_blockquote_text(self, text: str) -> str:
        pass

    @abstractmethod
    def get_blank_line_opening_tag_patterns(self) -> list[str]:
        pass

    @abstractmethod
    def get_blank_line_closing_tag_patterns(self) -> list[str]:
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
        formatted_text = self._get_formatted_text(
            text=text,
            entities=entities,
            offset=0,
            length=len(text)
        )
        lines = formatted_text.split("\n")
        line_index = 0
        opening_tag_patterns = self.get_blank_line_opening_tag_patterns()
        closing_tag_patterns = self.get_blank_line_closing_tag_patterns()

        while line_index < len(lines):
            line = lines[line_index]
            line_opening_tags = _get_blank_line_tags(line, patterns=opening_tag_patterns)

            if line_opening_tags:
                next_line_index = line_index + 1

                while True:
                    if lines[next_line_index]:
                        break
                    else:
                        next_line_index += 1

                lines[next_line_index] = "".join(line_opening_tags) + lines[next_line_index]
                lines[line_index] = ""
                line_index = next_line_index
            else:
                line_closing_tags = _get_blank_line_tags(line, patterns=closing_tag_patterns)

                if line_closing_tags:
                    previous_line_index = line_index - 1

                    while True:
                        if lines[previous_line_index]:
                            break
                        else:
                            previous_line_index -= 1

                    lines[previous_line_index] = (
                        lines[previous_line_index]
                        + "".join(line_closing_tags)
                    )
                    lines[line_index] = ""

            line_index += 1

        return "\n".join(lines)

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
            elif entity.type == message_entity_types.BLOCKQUOTE:
                formatted_text += self.get_blockquote_text(entity_text)
            elif entity.type == message_entity_types.EXPANDABLE_BLOCKQUOTE:
                formatted_text += self.get_expandable_blockquote_text(entity_text)

        if offset < length:
            formatted_text += self.get_escaped_text(
                get_text_without_surrogates(
                    text[offset:length]
                )
            )

        return formatted_text


def _get_blank_line_tags(line: str, patterns: list[str]) -> list[str]:
    tags = []

    while True:
        for i in patterns:
            match = re.match(i, line)

            if match is not None:
                tag = match.group()
                tags.append(tag)
                line = line.replace(tag, "", 1)
                break
        else:
            break

    if line:
        tags.clear()

    return tags
