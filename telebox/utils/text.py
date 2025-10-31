from telebox.bot.utils.utils import get_text_formatter


def get_text(template: str, parse_mode: str, /, **fields) -> str:
    formatter = get_text_formatter(parse_mode)
    fields = {
        name: formatter.get_escaped_text(str(value))
        for name, value in fields.items()
    }

    return template.format(**fields)


def get_text_with_surrogates(text: str) -> bytes:
    return text.encode("UTF-16-LE")


def get_text_without_surrogates(text: bytes) -> str:
    return text.decode("UTF-16-LE")
