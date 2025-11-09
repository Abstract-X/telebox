from telebox.bot.formatter import AbstractFormatter
from telebox.bot.formatters.html import HTMLFormatter
from telebox.bot.formatters.markdown import MarkdownFormatter


_markdown_formatter = MarkdownFormatter()
TEXT_FORMATTERS = {
    "html": HTMLFormatter(),
    "markdown": _markdown_formatter,
    "markdownv2": _markdown_formatter
}


def get_text_formatter(parse_mode: str) -> AbstractFormatter:
    return TEXT_FORMATTERS[parse_mode.lower()]


def get_text(template: str, parse_mode: str, /, **fields) -> str:
    formatter = get_text_formatter(parse_mode)
    fields = {
        name: formatter.get_escaped_text(str(value))
        for name, value in fields.items()
    }

    return template.format(**fields)
