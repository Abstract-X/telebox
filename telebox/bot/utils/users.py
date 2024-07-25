from typing import Optional


def get_full_name(first_name: str, last_name: Optional[str]) -> str:
    return f"{first_name} {last_name}" if last_name else first_name
