from typing import Optional

from telebox.bot.utils.formatters.formatter import AbstractFormatter
from telebox.bot.utils.formatting import get_escaped_html_text


class HTMLFormatter(AbstractFormatter):

    def get_escaped_text(self, text: str) -> str:
        return get_escaped_html_text(text)

    def get_bold_text(self, text: str) -> str:
        return f"<b>{text}</b>"

    def get_italic_text(self, text: str) -> str:
        return f"<i>{text}</i>"

    def get_underline_text(self, text: str) -> str:
        return f"<u>{text}</u>"

    def get_strikethrough_text(self, text: str) -> str:
        return f"<s>{text}</s>"

    def get_spoiler_text(self, text: str) -> str:
        return f"<tg-spoiler>{text}</tg-spoiler>"

    def get_text_link_text(self, text: str, link: str) -> str:
        return f'<a href="{link}">{text}</a>'

    def get_code_text(self, text: str) -> str:
        return f"<code>{text}</code>"

    def get_pre_text(self, text: str, language: Optional[str] = None) -> str:
        if language:
            text = f'<code class="language-{language}">{text}</code>'

        return f"<pre>{text}</pre>"
