import ops
from scenario import State


def test_install_status(ctx):
    state_in = State()

    state_out = ctx.run("install", state_in)

    assert ctx.unit_status_history == [
        ops.UnknownStatus(),
        ops.MaintenanceStatus("installing nginx..."),
        ops.MaintenanceStatus("setting up ufw rules..."),
    ]

    assert state_out.unit_status == ops.ActiveStatus()
