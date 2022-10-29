import random

import pytest


@pytest.fixture()
def chat_id() -> int:
    return random.randint(1, 100_000_000)


@pytest.fixture()
def user_id() -> int:
    return random.randint(1, 100_000_000)
