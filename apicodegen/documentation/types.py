from dataclasses import dataclass
from typing import Optional


@dataclass
class Field:
    name: str
    types: list[str]
    array_nesting: int
    description: str
    is_optional: bool
    value: Optional[str] = None


@dataclass
class Parameter:
    name: str
    types: list[str]
    array_nesting: int
    description: str
    is_optional: bool


@dataclass
class Type:
    name: str
    description: str
    fields: list[Field]
    types: list[str]
    is_union: bool


@dataclass
class Method:
    name: str
    result_types: list[str]
    result_array_nesting: int
    description: str
    parameters: list[Parameter]
