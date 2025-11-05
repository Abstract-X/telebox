from dataclasses import dataclass
from typing import Optional


@dataclass
class PreparedField:
    name: str
    types: list[str]
    type_hint: str
    description: str
    is_optional: bool
    value: Optional[str] = None


@dataclass
class PreparedParameter:
    name: str
    type_hint: str
    description: str
    is_optional: bool
    value_code: Optional[str] = None


@dataclass
class PreparedType:
    name: str
    module_name: str
    description: str
    fields: list[PreparedField]
    types: list[str]
    is_union: bool
    additional_code: Optional[str] = None


@dataclass
class PreparedMethod:
    name: str
    function_name: str
    description: str
    parameters: list[PreparedParameter]
    result_type_hint: str
    result_array_nesting: int
    result_contains_object: bool
    result_is_object: bool
    result_object_type: Optional[str] = None

    @property
    def required_parameters(self) -> list[PreparedParameter]:
        return [i for i in self.parameters if not i.is_optional]

    @property
    def optional_parameters(self) -> list[PreparedParameter]:
        return [i for i in self.parameters if i.is_optional]
