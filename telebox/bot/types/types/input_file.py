from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from telebox.bot.types.type import Type


@dataclass
class InputFile(Type):
    content: bytes = field(repr=False)
    name: Optional[str] = None


def get_input_file_by_path(path: Union[str, Path], name: Optional[str] = None) -> InputFile:
    path = Path(path)

    with path.open("rb") as stream:
        return InputFile(
            content=stream.read(),
            name=name or path.name
        )
