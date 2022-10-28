from unittest.mock import Mock

import pytest


@pytest.fixture(scope="session")
def token() -> str:
    return "123456789:DC3hu7d7Q1QuoLOowwpJ_iL1cIZsyw4EhQw"


@pytest.fixture()
def session_mock() -> Mock:
    return Mock()
