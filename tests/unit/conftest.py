from unittest.mock import MagicMock, patch

import pytest
from charm import IntroToCharmingMcCharm
from scenario import Context


@pytest.fixture
def ctx():
    procmock = MagicMock()
    procmock.wait = lambda: True

    with patch.object(IntroToCharmingMcCharm, "_run_local", return_value=procmock):
        yield Context(IntroToCharmingMcCharm)
