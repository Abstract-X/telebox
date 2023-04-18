from typing import Optional

from telebox.bot.utils.formatters.formatter import AbstractFormatter
from telebox.bot.utils.formatting import get_escaped_markdown_text


class MarkdownFormatter(AbstractFormatter):

    def get_escaped_text(self, text: str) -> str:
        return get_escaped_markdown_text(text)

    def get_bold_text(self, text: str) -> str:
        return f"*{text}*"

    def get_italic_text(self, text: str) -> str:
        return f"_\r{text}_\r"

    def get_underline_text(self, text: str) -> str:
        return f"__\r{text}__\r"

    def get_strikethrough_text(self, text: str) -> str:
        return f"~{text}~"

    def get_spoiler_text(self, text: str) -> str:
        return f"||{text}||"

    def get_text_link_text(self, text: str, link: str) -> str:
        return f'[{text}]({link})'

    def get_code_text(self, text: str) -> str:
        return f"`{text}`"

    def get_pre_text(self, text: str, language: Optional[str] = None) -> str:
        return f"```{language or ''}\n{text}\n```"
