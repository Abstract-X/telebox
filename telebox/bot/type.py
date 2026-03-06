import attrs
from attrs import define

from telebox.bot.converter import converting_context
from telebox.unset import UNSET


def default_factory():
    if converting_context.get():
        return None

    return UNSET


@define(repr=False)
class Type:
    def __repr__(self) -> str:
        values = {}

        for i in attrs.fields(type(self)):
            if not i.repr or not i.init:
                continue

            value = getattr(self, i.name)

            if value is not None:
                values[i.name] = value

        type_name = type(self).__name__
        values = ", ".join(
            f"{name}={value!r}" for name, value in values.items()
        )

        return f"{type_name}({values})"
