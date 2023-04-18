from abc import ABC, abstractmethod
from typing import Optional

from telebox.bot.utils.deep_links import get_user_link


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
