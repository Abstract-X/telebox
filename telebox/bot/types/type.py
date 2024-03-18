import dataclasses
from dataclasses import dataclass


@dataclass
class Type:

    def __repr__(self) -> str:
        values = {}

        for i in dataclasses.fields(self):
            value = getattr(self, i.name)

            if value is not None:
                values[i.name] = value

        type_name = type(self).__name__
        values = ", ".join(
            f"{name}={value!r}" for name, value in values.items()
        )

        return f"{type_name}({values})"
