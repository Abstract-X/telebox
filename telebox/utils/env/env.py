from dataclasses import dataclass

from telebox.utils.env.errors import EnvError


@dataclass
class Env:

    def initialize(self, **kwargs) -> None:
        for name, value in kwargs.items():
            if name not in vars(self):
                raise EnvError(f"No {name!r} field!")

            setattr(self, name, value)

        for name, value in vars(self).items():
            if value is None:
                raise EnvError(f"{name!r} is not set!")
