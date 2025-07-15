import dataclasses
from typing import Type, TypeVar, Any, Optional
from datetime import datetime as datetime_, timezone

from cattrs import Converter

from telebox.bot.types.types.input_file import InputFile
from telebox.utils.not_set import NotSet, NOT_SET


DataclassObject = TypeVar("DataclassObject")


def get_timestamp(datetime: Optional[datetime_]) -> int:
    return int(datetime.timestamp()) if datetime is not None else 0


def get_datetime(timestamp: int) -> Optional[datetime_]:
    return datetime_.fromtimestamp(timestamp, tz=timezone.utc) if timestamp else None


class DataclassConverter:

    # noinspection PyMethodMayBeStatic
    def get_object(
        self,
        data: dict[str, Any],
        class_: Type[DataclassObject]
    ) -> DataclassObject:
        return _converter.structure(data, class_)

    # noinspection PyMethodMayBeStatic
    def get_data(self, object_: Any) -> dict[str, Any]:
        return _converter.unstructure(object_)


def _get_without_none(object_: Any) -> Any:
    if not dataclasses.is_dataclass(object_):
        return object_

    data = {}

    for i in dataclasses.fields(object_):
        value = getattr(object_, i.name)

        if value is not None:
            data[i.name] = _converter.unstructure(value)

    return data


def _get_converter() -> Converter:
    converter = Converter()
    converter.register_unstructure_hook_func(dataclasses.is_dataclass, _get_without_none)
    converter.register_unstructure_hook(datetime_, get_timestamp)
    converter.register_unstructure_hook(InputFile, lambda file: file)
    converter.register_unstructure_hook(NotSet, lambda not_set: NOT_SET)
    converter.register_structure_hook(datetime_, lambda datetime, _: get_datetime(datetime))
    converter.register_structure_hook(InputFile, lambda file, _: file)
    converter.register_structure_hook(NotSet, lambda not_set, _: NOT_SET)

    return converter


_converter = _get_converter()
