from typing import Optional
import html

from telebox.bot.utils.formatter import AbstractFormatter


class HTMLFormatter(AbstractFormatter):
    def get_escaped_text(self, text: str) -> str:
        return html.escape(text, quote=False)

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

    def get_blockquote_text(self, text: str) -> str:
        return f"<blockquote>{text}</blockquote>"

    def get_expandable_blockquote_text(self, text: str) -> str:
        return f"<blockquote expandable>{text}</blockquote>"

    def get_blank_line_opening_tag_patterns(self) -> list[str]:
        return [
            "<b>",
            "<i>",
            "<u>",
            "<s>",
            r"<tg\-spoiler>",
            r"""<a href=(\'|\").*?(\'|\")>"""
            "<code>",
            "<pre>",
            "<blockquote>",
            "<blockquote expandable>"
        ]

    def get_blank_line_closing_tag_patterns(self) -> list[str]:
        return [
            "</b>",
            "</i>",
            "</u>",
            "</s>",
            r"</tg\-spoiler>",
            "</a>",
            "</code>",
            "</pre>",
            "</blockquote>"
        ]
