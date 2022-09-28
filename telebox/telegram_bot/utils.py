from typing import Optional
from base64 import urlsafe_b64encode, urlsafe_b64decode


def get_url(path: Optional[str] = None) -> str:
    url = f"https://t.me/"

    if path is not None:
        url += path

    return url


def get_user_mention_url(id_: int) -> str:
    return f"tg://user?id={id_}"


def get_message_public_url(path: str, message_id: int) -> str:
    return get_url(f"{path}/{message_id}")


def get_message_private_url(chat_id: int, message_id: int) -> str:
    return get_url(f"c/{chat_id}/{message_id}")


def get_chat_id_with_prefix(id_: int) -> int:
    if id_ > 0:
        id_without_prefix = id_
        multiplier = 1

        while id_without_prefix:
            id_without_prefix //= 10
            multiplier *= 10

        return -id_ + -100 * multiplier
    elif id_ == 0:
        return -100_0

    return id_


def get_chat_id_without_prefix(id_: int) -> int:
    if id_ <= -100_0:
        id_with_prefix = id_
        multiplier = 1

        while id_with_prefix != -100:
            id_with_prefix = -(id_with_prefix // -10)
            multiplier *= 10

            if not id_with_prefix:
                break
        else:
            return -100 * multiplier - id_

    return id_


def get_full_name(first_name: str, last_name: Optional[str]) -> str:
    full_name = first_name

    if last_name is not None:
        full_name += f" {last_name}"

    return full_name


def get_attach_string(name: str) -> str:
    return f"attach://{name}"


def get_encoded_deep_link_payload(payload: str) -> str:
    return urlsafe_b64encode(payload.encode()).decode()


def get_decoded_deep_link_payload(payload: str) -> str:
    return urlsafe_b64decode(payload.encode()).decode()


def get_start_deep_link(username: str, payload: str, encode: bool = False) -> str:
    return _get_deep_link("start", username, payload, encode)


def get_startgroup_deep_link(username: str, payload: str, encode: bool = False) -> str:
    return _get_deep_link("startgroup", username, payload, encode)


def _get_deep_link(type_: str, username: str, payload: str, encode: bool) -> str:
    if encode:
        payload = get_encoded_deep_link_payload(payload)

    return get_url(f"{username}?{type_}={payload}")
