import urllib.parse
from typing import Any
import hashlib
import hmac

from telebox.bot.utils.converters import DataclassConverter
from telebox.bot.types.types.web_app_init_data import WebAppInitData
from telebox.utils.serialization import get_deserialized_data


_dataclass_converter = DataclassConverter()


def check_web_app_init_data(data: str, token: str, *, with_exceptions: bool = False) -> bool:
    try:
        data = _get_parsed_init_data(data)
        hash_ = data.pop("hash")
        data_check_string = "\n".join(
            f"{name}={value}"
            for name, value in sorted(
                data.items(),
                key=lambda i: i[0]
            )
        )
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=token.encode(
                encoding="UTF-8"
            ),
            digestmod=hashlib.sha256
        )
        calculated_hash = hmac.new(
            key=secret_key.digest(),
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        return hash_ == calculated_hash
    except Exception as error:
        if with_exceptions:
            raise error from None

        return False


def get_web_app_init_data(data: str) -> WebAppInitData:
    data = _get_parsed_init_data(data)

    for name in ("user", "receiver", "chat"):
        value = data.get(name)

        if value:
            data[name] = get_deserialized_data(value)

    _set_empty_string_none(data)
    data["auth_date"] = int(data["auth_date"])
    can_send_after = data.get("can_send_after")

    if can_send_after is not None:
        data["can_send_after"] = int(can_send_after)

    return _dataclass_converter.get_object(
        data=data,
        class_=WebAppInitData
    )


def _get_parsed_init_data(data: str) -> dict[str, Any]:
    return dict(
        urllib.parse.parse_qsl(
            data,
            strict_parsing=True,
            encoding="UTF-8"
        )
    )


def _set_empty_string_none(data: dict[str, Any]) -> None:
    for name, value in data.items():
        if isinstance(value, dict):
            _set_empty_string_none(value)
        elif value == "":
            data[name] = None
