from dataclasses import dataclass

from telebox.utils.env.errors import EnvError


@dataclass
class Env:

    def check_vars(self) -> None:
        for name, value in vars(self).items():
            if value is None:
                raise EnvError(f"{name!r} is not set!")
