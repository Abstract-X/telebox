from typing import Iterable, get_type_hints


class DepsError(Exception):
    pass


class DepsBase:
    def __init__(self, **deps):
        self.__check_deps(deps)
        self.__deps = deps

    def __getattr__(self, item):
        try:
            return self.__deps[item]
        except KeyError:
            if item in self.__get_fields():
                text = f"{item!r} dependency is not set!"
            else:
                text = f"Unknown dependency {item!r}!"

            raise DepsError(text) from None

    def __dir__(self) -> Iterable[str]:
        attributes = list(super().__dir__())
        attributes.extend(self.__deps)

        return attributes

    def __repr__(self):
        class_name = type(self).__name__
        field_text = ", ".join(f"{name}={value!r}" for name, value in self.__deps.items())

        return f"{class_name}({field_text})"

    def initialize(self, **deps) -> None:
        self.__check_deps(deps)
        self.__deps.update(deps)

        for i in self.__get_fields():
            if i not in self.__deps:
                raise DepsError(f"{i!r} dependency is not set!")

    @classmethod
    def __get_fields(cls) -> set[str]:
        return set(get_type_hints(cls))

    @classmethod
    def __check_deps(cls, deps: Iterable[str]) -> None:
        fields = cls.__get_fields()

        for i in deps:
            if i not in fields:
                raise DepsError(f"Unknown dependency {i!r}!")
