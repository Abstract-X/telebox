from typing import Optional, Any, Iterable
from urllib.parse import urlencode

from telebox.utils.not_set import NOT_SET


def get_username_link(username: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username
            }
        )
    else:
        return f"t.me/{username}"


def get_phone_number_link(number: str, *, with_tg: bool = False) -> str:
    number = number.lstrip("+")

    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "phone": number
            }
        )
    else:
        return f"t.me/+{number}"


def get_chat_invite_link(hash_: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://join",
            parameters={
                "invite": hash_
            }
        )
    else:
        return f"t.me/+{hash_}"


def get_message_public_link(username: str, message_id: int, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "post": message_id
            }
        )
    else:
        return f"t.me/{username}/{message_id}"


def get_message_private_link(chat_id: int, message_id: int, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://privatepost",
            parameters={
                "channel": chat_id,
                "post": message_id
            }
        )
    else:
        return f"t.me/c/{chat_id}/{message_id}"


def get_share_link(url: str, text: Optional[str] = None, *, with_tg: bool = False) -> str:
    return _get_parametrized_link(
        "tg://msg_url" if with_tg else "t.me/share",
        parameters={
            "url": url,
            "text": text
        }
    )


def get_video_chat_link(
    username: str,
    invite_hash: Optional[str] = None,
    *,
    with_tg: bool = False
) -> str:
    video_chat_value = NOT_SET if invite_hash is None else invite_hash

    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "videochat": video_chat_value
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "videochat": video_chat_value
            }
        )


def get_livestream_link(
    username: str,
    invite_hash: Optional[str] = None,
    *,
    with_tg: bool = False
) -> str:
    livestream_value = NOT_SET if invite_hash is None else invite_hash

    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "livestream": livestream_value
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "livestream": livestream_value
            }
        )


def get_voice_chat_link(
    username: str,
    invite_hash: Optional[str] = None,
    *,
    with_tg: bool = False
) -> str:
    voice_chat_value = NOT_SET if invite_hash is None else invite_hash

    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "voicechat": voice_chat_value
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "voicechat": voice_chat_value
            }
        )


def get_add_stickers_link(name: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://addstickers",
            parameters={
                "set": name
            }
        )
    else:
        return f"t.me/addstickers/{name}"


def get_add_emoji_link(name: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://addemoji",
            parameters={
                "set": name
            }
        )
    else:
        return f"t.me/addemoji/{name}"


def get_mtproxy_link(host: str, port: int, secret: str, *, with_tg: bool = False) -> str:
    return _get_parametrized_link(
        "tg://proxy" if with_tg else "t.me/proxy",
        parameters={
            "server": host,
            "port": port,
            "secret": secret
        }
    )


def get_socks5_proxy_link(
    host: str,
    port: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    *,
    with_tg: bool = False
) -> str:
    return _get_parametrized_link(
        "tg://socks" if with_tg else "t.me/socks",
        parameters={
            "server": host,
            "port": port,
            "user": username,
            "pass": password
        }
    )


def get_add_theme_link(name: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://addtheme",
            parameters={
                "slug": name
            }
        )
    else:
        return f"t.me/addtheme/{name}"


def get_bot_link(username: str, payload: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "start": payload
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "start": payload
            }
        )


def get_group_bot_link(
    username: str,
    payload: Optional[str] = None,
    admin_rights: Optional[Iterable[str]] = None,
    *,
    with_tg: bool = False
) -> str:
    payload_value = NOT_SET if payload is None else payload
    admin_value = "+".join(admin_rights) if admin_rights is not None else None

    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "startgroup": payload_value,
                "admin": admin_value
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "startgroup": payload_value,
                "admin": admin_value
            }
        )


def get_channel_bot_link(
    username: str,
    admin_rights: Iterable[str],
    *,
    with_tg: bool = False
) -> str:
    admin_value = "+".join(admin_rights)

    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "startchannel": NOT_SET,
                "admin": admin_value
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "startchannel": NOT_SET,
                "admin": admin_value
            }
        )


def get_game_link(username: str, name: str, *, with_tg: bool = False) -> str:
    if with_tg:
        return _get_parametrized_link(
            "tg://resolve",
            parameters={
                "domain": username,
                "game": name
            }
        )
    else:
        return _get_parametrized_link(
            f"t.me/{username}",
            parameters={
                "game": name
            }
        )


def get_user_link(id_: int) -> str:
    return _get_parametrized_link(
        "tg://user",
        parameters={
            "id": id_
        }
    )


def _get_parametrized_link(uri: str, parameters: dict[str, Any]) -> str:
    value_parameters = {}
    no_value_parameters = []

    for name, value in parameters.items():
        if value is NOT_SET:
            no_value_parameters.append(name)
        elif value is not None:
            value_parameters[name] = value

    link = uri

    if value_parameters or no_value_parameters:
        link += "?"

        if value_parameters:
            link += urlencode(value_parameters, encoding="UTF-8")

            if no_value_parameters:
                link += "&" + "&".join(no_value_parameters)
        elif no_value_parameters:
            link += "&".join(no_value_parameters)

    return link
