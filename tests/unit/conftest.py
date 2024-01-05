from unittest.mock import MagicMock, patch

import pytest
from scenario import Context

from charm import IntroToCharmingMcCharm


@pytest.fixture
def ctx():
    procmock = MagicMock()
    procmock.wait = lambda: True

    with patch.object(IntroToCharmingMcCharm, "_run_local", return_value=procmock):
        yield Context(IntroToCharmingMcCharm)
