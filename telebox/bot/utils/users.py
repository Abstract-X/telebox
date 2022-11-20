from typing import Optional


def get_full_name(first_name: str, last_name: Optional[str]) -> str:
    return f"{first_name} {last_name}" if last_name is not None else first_name
