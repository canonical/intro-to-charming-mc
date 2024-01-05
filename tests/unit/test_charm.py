from unittest.mock import MagicMock, patch

import ops
import pytest
from charm import IntroToCharmingMcCharm
from scenario import Context, State


@pytest.fixture
def ctx():
    procmock = MagicMock()
    procmock.wait = lambda: True

    with patch.object(IntroToCharmingMcCharm, "_run_local", return_value=procmock):
        yield Context(IntroToCharmingMcCharm)


def test_install_status(ctx):
    state_in = State()

    state_out = ctx.run("install", state_in)

    assert ctx.unit_status_history == [
        ops.UnknownStatus(),
        ops.MaintenanceStatus("installing nginx..."),
        ops.MaintenanceStatus("setting up ufw rules..."),
    ]

    assert state_out.unit_status == ops.ActiveStatus()
