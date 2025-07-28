import typing
from typing import Type, TypeVar, Any, Optional, Union
from datetime import datetime as datetime_, timezone

import attrs
import cattrs
from cattrs.gen import make_dict_unstructure_fn, make_dict_structure_fn, override

from telebox.bot.types.type import Type as Type_
from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.input_message_content import InputMessageContent
from telebox.bot.types.types.inline_query_result import InlineQueryResult
from telebox.bot.types.types.transaction_partner import TransactionPartner
from telebox.bot.types.types.revenue_withdrawal_state import RevenueWithdrawalState
from telebox.bot.types.types.maybe_inaccessible_message import MaybeInaccessibleMessage
from telebox.bot.types.types.chat_member import ChatMember
from telebox.bot.types.types.chat_boost_source import ChatBoostSource
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.inaccessible_message import InaccessibleMessage
from telebox.utils.not_set import NotSet, NOT_SET


Object = TypeVar("Object")


def _get_types(type_: type):
    origin_type = typing.get_origin(type_)

    if origin_type is Union:
        types = typing.get_args(type_)
    else:
        types = (type_,)

    return types


def _get_non_structuring_types():
    types = [NotSet, InputFile, InputMessageContent]

    for type_ in types[:]:
        for i in _get_types(type_):
            if issubclass(i, Type_):
                types.append(i)

    return types


NON_STRUCTURING_TYPES = _get_non_structuring_types()


def get_timestamp(datetime: Optional[datetime_]) -> int:
    return int(datetime.timestamp()) if datetime is not None else 0


def get_datetime(timestamp: int) -> Optional[datetime_]:
    return datetime_.fromtimestamp(timestamp, tz=timezone.utc) if timestamp else None


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance


class Converter(metaclass=Singleton):
    def __init__(self):
        self._converter = cattrs.Converter()
        self._converter.register_unstructure_hook_factory(
            attrs.has,
            self._unstructure_hook_factory
        )

        for type_, hook in (
            (datetime_, get_timestamp),
            (InputFile, lambda file: file),
            (NotSet, lambda not_set: NOT_SET)
        ):
            self._converter.register_unstructure_hook(type_, hook)

        self._converter.register_structure_hook_factory(
            attrs.has,
            self._structure_hook_factory
        )
        self._register_optional_structure_hook(
            class_=MaybeInaccessibleMessage,
            hook=self._get_maybe_inaccessible_message
        )

        for type_, name in (
            (ChatMember, "status"),
            (ChatBoostSource, "source"),
            (TransactionPartner, "type"),
            (RevenueWithdrawalState, "type"),
            (InlineQueryResult, "type")
        ):
            self._register_union_type_structure_hook(type_, name)

        for type_, hook in (
            (datetime_, lambda datetime, _: get_datetime(datetime)),
            (InputFile, lambda file, _: file),
            (NotSet, lambda not_set, _: NOT_SET),
            (Union[int, str], lambda value, _: value),
            (Union[int, str, None], lambda value, _: value)
        ):
            self._converter.register_structure_hook(type_, hook)

    def get_object(
        self,
        data: dict[str, Any],
        class_: Type[Object]
    ) -> Object:
        return self._converter.structure(data, class_)

    def get_data(self, object_: Any) -> dict[str, Any]:
        return self._converter.unstructure(object_)

    def check_class(self, class_: type) -> bool:
        return attrs.has(class_)

    def check_class_fields(self, class_: type) -> None:
        if not self.check_class(class_):
            raise TypeError(f"Class {class_!r} is not supported!")

        if not _check_structuring_type(class_):
            return

        fields = attrs.fields(class_)
        structuring_fields = []
        unstructuring_fields = []

        for i in fields:
            if i.init:
                if _check_structuring_type(i.type):
                    structuring_fields.append(i)

                unstructuring_fields.append(i)

        for i in structuring_fields:
            try:
                self._converter._structure_func.dispatch(i.type)
            except Exception:
                raise ValueError(
                    f"Structuring field {class_.__name__}.{i.name} "
                    f"has an unsupported type {i.type!r}!"
                ) from None

        for i in unstructuring_fields:
            try:
                self._converter._unstructure_func.dispatch(i.type)
            except Exception:
                raise ValueError(
                    f"Unstructuring field {class_.__name__}.{i.name} "
                    f"has an unsupported type {i.type!r}!"
                ) from None

    def _unstructure_hook_factory(self, class_):
        base_unstructure = make_dict_unstructure_fn(
            class_,
            self._converter,
            **_get_renamed_fields(class_)
        )

        def hook(object_):
            data = base_unstructure(object_)

            return {
                name: value
                for name, value in data.items()
                if value is not None
            }

        return hook

    def _structure_hook_factory(self, class_):
        return make_dict_structure_fn(
            class_,
            self._converter,
            **_get_renamed_fields(class_)
        )

    def _register_optional_structure_hook(self, class_, hook) -> None:
        self._converter.register_structure_hook(
            class_,
            lambda object_, _: hook(object_)
        )
        self._converter.register_structure_hook(
            Optional[class_],
            lambda object_, _: None if object_ is None else hook(object_)
        )

    def _register_union_type_structure_hook(self, class_, name: str) -> None:
        hook = self._union_type_getter_factory(class_, name)
        self._register_optional_structure_hook(class_, hook)

    def _union_type_getter_factory(self, class_: Type_, name: str):
        types = {}

        for inner_type in typing.get_args(class_):
            for i in attrs.fields(inner_type):
                if i.name == name:
                    types[i.default] = inner_type
                    break
            else:
                raise TypeError(inner_type)

        def get_type(data: dict):
            return self._converter.structure(data, types[data[name]])

        return get_type

    def _get_maybe_inaccessible_message(self, data: dict) -> MaybeInaccessibleMessage:
        if data["date"] == 0:
            return self._converter.structure(data, InaccessibleMessage)

        return self._converter.structure(data, Message)


def _get_renamed_fields(class_) -> dict[str, Any]:
    return {
        field.name: override(rename=field.name.removesuffix("_"))
        for field in attrs.fields(class_)
        if field.name.endswith("_")
    }


def _check_structuring_type(type_: type) -> bool:
    for i in _get_types(type_):
        if i in NON_STRUCTURING_TYPES:
            return False

    return True
