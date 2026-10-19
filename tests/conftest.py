import pytest

from app.model import train


@pytest.fixture(scope="session", autouse=True)
def trained_model():
    train()
