import typing
from typing import Type, TypeVar, Any, Optional, Union
from datetime import datetime as datetime_, timezone
from contextvars import ContextVar  # noqa

import attrs
import cattrs
from cattrs.strategies import configure_union_passthrough
from cattrs.gen import make_dict_unstructure_fn, make_dict_structure_fn, override  # noqa

from telebox.unset import Unset, UNSET
from telebox.bot.default_parameters import DefaultParameterSet


Object = TypeVar("Object")
converting_context = ContextVar("converting_context", default=False)


def _get_types(type_: type):
    origin_type = typing.get_origin(type_)

    if origin_type is Union:
        types = typing.get_args(type_)
    else:
        types = (type_,)

    return types


def get_timestamp(datetime: Optional[datetime_]) -> int:
    return int(datetime.timestamp()) if datetime is not None else 0


def get_datetime(timestamp: int) -> Optional[datetime_]:
    return datetime_.fromtimestamp(timestamp, tz=timezone.utc) if timestamp else None


class Converter:
    def __init__(self, default_parameters: DefaultParameterSet):
        self.default_parameters = default_parameters
        self._converter = cattrs.Converter(detailed_validation=False)
        self._set_structure_parameters()
        self._set_unstructure_parameters()

    def get_object(
        self,
        data: dict[str, Any],
        class_: Type[Object]
    ) -> Object:
        token = converting_context.set(True)

        try:
            return self._converter.structure(data, class_)
        finally:
            converting_context.reset(token)

    def get_data(self, object_: Any) -> dict[str, Any]:
        return self._converter.unstructure(object_)

    def check_class(self, class_: type) -> bool:  # noqa
        return attrs.has(class_)

    def _set_structure_parameters(self) -> None:
        from telebox.bot.types.maybe_inaccessible_message import MaybeInaccessibleMessage
        from telebox.bot.types.inaccessible_message import InaccessibleMessage
        from telebox.bot.types.input_file import InputFile
        from telebox.bot.types.message import Message

        def _get_maybe_inaccessible_message(data: dict) -> MaybeInaccessibleMessage:
            if data["date"] == 0:
                return self._converter.structure(data, InaccessibleMessage)

            return self._converter.structure(data, Message)

        configure_union_passthrough(Union[Unset, InputFile], self._converter)
        self._converter.register_structure_hook_factory(
            attrs.has,
            self._structure_hook_factory
        )

        for type_, hook in (
            (MaybeInaccessibleMessage, lambda data, _: _get_maybe_inaccessible_message(data)),
            (datetime_, lambda data, _: get_datetime(data))
        ):
            self._converter.register_structure_hook(type_, hook)

    def _set_unstructure_parameters(self) -> None:
        from telebox.bot.types.input_file import InputFile

        self._converter.register_unstructure_hook_factory(
            attrs.has,
            self._unstructure_hook_factory
        )

        for type_, hook in (
            (datetime_, get_timestamp),
            (InputFile, lambda file: file)
        ):
            self._converter.register_unstructure_hook(type_, hook)

    def _unstructure_hook_factory(self, class_):
        base_unstructure = make_dict_unstructure_fn(
            class_,
            self._converter,
            **_get_renamed_fields(class_)
        )

        def hook(object_):
            data = base_unstructure(object_)
            prepared_data = {}

            for name, value in data.items():
                prepared_value = value

                if (
                    name.endswith("parse_mode")
                    and (value is UNSET)
                    and self.default_parameters.parse_mode
                ):
                    prefix = name.removesuffix("parse_mode")

                    if prefix:
                        entities_field_names = (f"{prefix}entities",)
                    else:
                        entities_field_names = ("entities", "caption_entities")

                    for i in data:
                        if i in entities_field_names:
                            entities_field = i
                            break
                    else:
                        raise ValueError(f"No entities field for {prefix!r} prefix!")

                    if not data[entities_field]:
                        prepared_value = self.default_parameters.parse_mode
                elif (
                    (name == "resize_keyboard")
                    and (value is UNSET)
                    and self.default_parameters.resize_reply_keyboard
                ):
                    prepared_value = True

                if prepared_value is not None and prepared_value is not UNSET:
                    prepared_data[name] = prepared_value

            return prepared_data

        return hook

    def _structure_hook_factory(self, class_):
        return make_dict_structure_fn(
            class_,
            self._converter,
            **_get_renamed_fields(class_)
        )


def _get_renamed_fields(class_) -> dict[str, Any]:
    return {
        field.name: override(rename=field.name.removesuffix("_"))
        for field in attrs.fields(class_)
        if field.name.endswith("_")
    }
