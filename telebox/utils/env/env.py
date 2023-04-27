from typing import Iterable, get_type_hints

from telebox.utils.env.errors import EnvError


class Env:

    def __init__(self, **fields):
        self.__check_fields(fields)
        self.__fields = fields

    def __getattr__(self, item):
        try:
            return self.__fields[item]
        except KeyError:
            if item in self.__get_fields():
                text = f"{item!r} field is not set!"
            else:
                text = f"Unknown field {item!r}!"

            raise EnvError(text) from None

    def __dir__(self) -> Iterable[str]:
        attributes = list(super().__dir__())
        attributes.extend(self.__fields)

        return attributes

    def __repr__(self):
        class_name = type(self).__name__
        field_text = ", ".join(f"{name}={value!r}" for name, value in self.__fields.items())

        return f"{class_name}({field_text})"

    def initialize(self, **fields) -> None:
        self.__check_fields(fields)
        self.__fields.update(fields)

        for i in self.__get_fields():
            if i not in self.__fields:
                raise EnvError(f"{i!r} field is not set!")

    @classmethod
    def __get_fields(cls) -> set[str]:
        return set(get_type_hints(cls))

    @classmethod
    def __check_fields(cls, fields: Iterable[str]) -> None:
        class_fields = cls.__get_fields()

        for i in fields:
            if i not in class_fields:
                raise EnvError(f"Unknown field {i!r}!")
