from telebox.bot.consts import chat_types


_PREFIXES = {
    chat_types.GROUP: "-",
    chat_types.SUPERGROUP: "-100",
    chat_types.CHANNEL: "-100"
}


def get_prefixed_chat_id(chat_id: int, chat_type: str) -> int:
    try:
        prefix = _PREFIXES[chat_type]
    except KeyError:
        return chat_id

    if str(chat_id).startswith(prefix):
        return chat_id

    return int(f"{prefix}{chat_id}")


def get_unprefixed_chat_id(chat_id: int, chat_type: str) -> int:
    try:
        prefix = _PREFIXES[chat_type]
    except KeyError:
        return chat_id

    return int(str(chat_id).removeprefix(prefix))
