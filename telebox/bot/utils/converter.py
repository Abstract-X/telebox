from typing import Type, TypeVar, Any, Optional
from datetime import datetime as datetime_, timezone

import attrs
import cattrs
from cattrs.gen import make_dict_unstructure_fn, make_dict_structure_fn, override

from telebox.bot.types.types.input_file import InputFile
from telebox.bot.types.types.maybe_inaccessible_message import MaybeInaccessibleMessage
from telebox.bot.types.types.message import Message
from telebox.bot.types.types.inaccessible_message import InaccessibleMessage
from telebox.utils.not_set import NotSet, NOT_SET


Object = TypeVar("Object")


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
        self._converter.register_unstructure_hook(datetime_, get_timestamp)
        self._converter.register_unstructure_hook(InputFile, lambda file: file)
        self._converter.register_unstructure_hook(NotSet, lambda not_set: NOT_SET)

        self._converter.register_structure_hook_factory(
            attrs.has,
            self._structure_hook_factory
        )
        self._register_optional_structure_hook(
            class_=MaybeInaccessibleMessage,
            hook=self._get_maybe_inaccessible_message
        )
        self._converter.register_structure_hook(
            datetime_,
            lambda datetime, _: get_datetime(datetime)
        )
        self._converter.register_structure_hook(InputFile, lambda file, _: file)
        self._converter.register_structure_hook(NotSet, lambda not_set, _: NOT_SET)

    def get_object(
        self,
        data: dict[str, Any],
        class_: Type[Object]
    ) -> Object:
        return self._converter.structure(data, class_)

    def get_data(self, object_: Any) -> dict[str, Any]:
        return self._converter.unstructure(object_)

    def check_object(self, object_) -> bool:
        return attrs.has(type(object_))

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

    def _get_maybe_inaccessible_message(self, object_: dict) -> MaybeInaccessibleMessage:
        if object_["date"] == 0:
            return self._converter.structure(object_, InaccessibleMessage)

        return self._converter.structure(object_, Message)


def _get_renamed_fields(class_) -> dict[str, Any]:
    return {
        field.name: override(rename=field.name.removesuffix("_"))
        for field in attrs.fields(class_)
        if field.name.endswith("_")
    }
