from typing import Callable

from telebox.bot.utils.formatting import get_escaped_html_text, get_escaped_markdown_text


def get_html_text(template: str, /, *args, **kwargs) -> str:
    return _get_formatted_text(get_escaped_html_text, template, *args, **kwargs)


def get_markdown_text(template: str, /, *args, **kwargs) -> str:
    return _get_formatted_text(get_escaped_markdown_text, template, *args, **kwargs)


def get_text_with_surrogates(text: str) -> bytes:
    return text.encode("UTF-16-LE")


def get_text_without_surrogates(text: bytes) -> str:
    return text.decode("UTF-16-LE")


def _get_formatted_text(
    escaping_func: Callable[[str], str],
    template: str,
    /,
    *args,
    **kwargs
) -> str:
    args = tuple(escaping_func(str(i)) for i in args)
    kwargs = {
        name: escaping_func(str(value))
        for name, value in kwargs.items()
    }

    return template.format(*args, **kwargs)
