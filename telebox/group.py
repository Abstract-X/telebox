from dataclasses import dataclass
import dataclasses
import importlib
import pkgutil
import inspect
from typing import Any, Optional

from telebox.errors import TeleboxError


class UnknownFieldNameError(TeleboxError):
    def __init__(self, message: str = "", *, name: str):
        super().__init__(message=message)
        self.name = name


class ClassNotFoundError(TeleboxError):
    def __init__(self, message: str = "", *, field: str):
        super().__init__(message=message)
        self.field = field


@dataclass
class Group:
    def __post_init__(self):
        self._items = _get_items(self)

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return bool(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return f"{type(self).__name__}({self._items!r})"

    def __contains__(self, item):
        return item in self._items

    def get(self, *excluded: Any) -> set[Any]:
        return {i for i in self._items if i not in excluded}


def get_group(
    type_: type[Group],
    package_path: str,
    *,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
    names: Optional[dict[str, str]] = None,
    postfix: Optional[str] = None
) -> Group:
    args = args or ()
    kwargs = kwargs or {}
    names = _get_item_names(type_, names, postfix)
    items = {}
    _set_items(
        items=items,
        names=names,
        package_path=package_path,
        args=args,
        kwargs=kwargs
    )

    for i in names.values():
        if i not in items:
            raise ClassNotFoundError(f"Class for field {i!r} not found!", field=i)

    return type_(**items)


def _get_pascal_case_name(name: str) -> str:
    return "".join(
        i.title() for i in name.split("_")
    )


def _get_item_names(
    type_: type[Group],
    names: Optional[dict[str, str]] = None,
    postfix: Optional[str] = None
) -> dict[str, str]:
    names_ = {}

    for i in dataclasses.fields(type_):
        class_name = _get_pascal_case_name(
            i.name.strip("_")
        )
        names_[class_name] = i.name

    if postfix:
        names_ = {
            class_name + postfix: field_name
            for class_name, field_name in names_.items()
        }

    if names:
        for field_name, class_name in names.items():
            if field_name not in names_.values():
                raise UnknownFieldNameError(f"Unknown field name {field_name!r}!", name=field_name)

            names_[class_name] = field_name

    return names_


def _set_items(
    items: dict[str, Any],
    names: dict[str, str],
    package_path: str,
    args: tuple,
    kwargs: dict
) -> None:
    package = importlib.import_module(package_path)

    for _, module_name, is_package in pkgutil.iter_modules(package.__path__):
        module_path = f"{package_path}.{module_name}"
        module = importlib.import_module(module_path)

        for name, object_ in inspect.getmembers(module):
            if inspect.isclass(object_):
                field_name = names.get(name)

                if (field_name is not None) and (field_name not in items):
                    items[field_name] = object_(*args, **kwargs)

        if is_package:
            _set_items(
                items=items,
                names=names,
                package_path=module_path,
                args=args,
                kwargs=kwargs
            )


def _get_items(group: Group) -> set[Any]:
    items = set()
    fields = {i.name for i in dataclasses.fields(group)}

    for name, value in vars(group).items():
        if name in fields:
            if isinstance(value, Group):
                items.update(
                    _get_items(value)
                )
            else:
                items.add(value)

    return items
