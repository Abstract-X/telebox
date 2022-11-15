import html
import re


_markdown_pattern = re.compile(r"([_*\[\]()~`>#+\-=|{}.!\\])")


def get_escaped_html_text(text: str) -> str:
    return html.escape(text, quote=False)


def get_escaped_markdown_text(text: str) -> str:
    return re.sub(_markdown_pattern, r"\\\1", text)
