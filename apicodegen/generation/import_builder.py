import sysconfig
from pathlib import Path
import importlib.util
from enum import IntEnum
from typing import Optional
from dataclasses import dataclass


stdlib_dir = Path(sysconfig.get_paths()["stdlib"])


class ImportType(IntEnum):
    STANDARD = 1
    THIRD_PARTY = 2
    LOCAL = 3
    TYPE_CHECKING = 4


@dataclass
class ImportSet:
    standard: list[str]
    third_party: list[str]
    local: list[str]
    type_checking: list[str]


class ImportBuilder:
    def __init__(self, *, exclude: Optional[tuple[str, str]] = None):
        self._exclude = exclude
        self._imports = {i: {} for i in ImportType}

    def add_import(self, module_path: str, entity: str, for_type_checking: bool = False) -> None:
        if (module_path, entity) == self._exclude:
            return

        if for_type_checking:
            self.add_import("typing", "TYPE_CHECKING")
            type_ = ImportType.TYPE_CHECKING

            if module_path in self._imports[ImportType.LOCAL]:
                try:
                    self._imports[ImportType.LOCAL][module_path].remove(entity)
                except ValueError:
                    pass
                else:
                    if not self._imports[ImportType.LOCAL][module_path]:
                        del self._imports[ImportType.LOCAL][module_path]
        else:
            type_ = _get_import_type(module_path)

            if (
                (type_ is ImportType.LOCAL)
                and (entity in self._imports[ImportType.TYPE_CHECKING].get(module_path, []))
            ):
                return

        if module_path not in self._imports[type_]:
            self._imports[type_][module_path] = []
        elif entity in self._imports[type_][module_path]:
            return

        self._imports[type_][module_path].append(entity)

    def check_import(self, module_path: str, entity: str) -> bool:
        for i in self._imports.values():
            if module_path in i and entity in i[module_path]:
                return True

        return False

    def get_imports(self) -> ImportSet:
        return ImportSet(
            standard=self._get_imports(ImportType.STANDARD),
            third_party=self._get_imports(ImportType.THIRD_PARTY),
            local=self._get_imports(ImportType.LOCAL),
            type_checking=self._get_imports(ImportType.TYPE_CHECKING)
        )

    def _get_imports(self, type_: ImportType) -> list[str]:
        imports = []

        for module_path, entities in self._imports[type_].items():
            imports.append(f"from {module_path} import {', '.join(entities)}")

        return sorted(imports)


def _get_import_type(module_path: str) -> ImportType:
    if module_path.startswith("."):
        return ImportType.LOCAL

    import_name = module_path.split(".", 1)[0]

    if import_name == "telebox":
        return ImportType.LOCAL
    elif _check_standard_import_name(import_name):
        return ImportType.STANDARD

    return ImportType.THIRD_PARTY


def _check_standard_import_name(import_name: str) -> bool:
    spec = importlib.util.find_spec(import_name)

    if spec is None:
        return False

    if spec.origin in ("built-in", "frozen"):
        return True

    return stdlib_dir in Path(spec.origin).parents
