# type: ignore

import pytest

from numidium.ui.application import Numidium


@pytest.fixture(scope="session")
def qapp():
    yield Numidium([])
