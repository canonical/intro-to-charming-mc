import ops
import pytest
from charm import IntroToCharmingMcCharm
from scenario import State, Context


@pytest.fixture
def ctx():
    return Context(IntroToCharmingMcCharm)


def test_install_statuse(ctx):
    state_in = State()

    state_out = ctx.run("install", state_in)

    assert ctx.unit_status_history == [
        ops.UnknownStatus(),
        ops.MaintenanceStatus("installing nginx..."),
        ops.MaintenanceStatus("setting up ufw rules..."),
    ]

    assert state_out.unit_status == ops.ActiveStatus()

