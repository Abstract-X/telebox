from telebox.bot.formatter import AbstractFormatter
from telebox.bot.formatters.html import HTMLFormatter
from telebox.bot.formatters.markdown import MarkdownFormatter


TEXT_FORMATTERS = {
    "html": HTMLFormatter(),
    "markdownv2": MarkdownFormatter()
}


def get_text_formatter(parse_mode: str) -> AbstractFormatter:
    return TEXT_FORMATTERS[parse_mode.lower()]


def get_html_text(template: str, /, **fields) -> str:
    return _get_text(template, "html", **fields)


def get_markdown_text(template: str, /, **fields) -> str:
    return _get_text(template, "markdownv2", **fields)


def _get_text(template: str, parse_mode: str, /, **fields) -> str:
    formatter = get_text_formatter(parse_mode)
    fields = {
        name: formatter.get_escaped_text(str(value))
        for name, value in fields.items()
    }

    return template.format(**fields)
