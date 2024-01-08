from unittest.mock import call

import ops
from scenario import State


def test_install_status(ctx, procmock):
    state_in = State()

    state_out = ctx.run("install", state_in)

    assert ctx.unit_status_history == [
        ops.UnknownStatus(),
        ops.MaintenanceStatus("installing nginx..."),
        ops.MaintenanceStatus("setting up ufw rules..."),
    ]

    assert state_out.unit_status == ops.ActiveStatus()

    procmock.assert_called()
    procmock.assert_has_calls(
        (
            call(["apt-get", "update", "-y"]),
            call(["apt-get", "install", "-y", "nginx"]),
            call(["ufw", "allow", "Nginx HTTP"]),
        ),
        any_order=True,
    )
