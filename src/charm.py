#!/usr/bin/env python3
# Copyright 2024 pietro
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following tutorial that will help you
develop a new k8s charm using the Operator Framework:

https://juju.is/docs/sdk/create-a-minimal-kubernetes-charm
"""

import logging
import shlex
from subprocess import Popen

import ops
from ops import MaintenanceStatus, ActiveStatus

logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class IntroToCharmingMcCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)

    def _on_install(self, event):
        self._install_nginx()  # this will also start it by default
        self._enable_nginx_firewall_profile()
        self.status = ActiveStatus()

    def _install_nginx(self):
        self.status = MaintenanceStatus("installing nginx...")

        script = (
            "apt update",
            "apt install nginx",
        )
        for line in script:
            proc = Popen(shlex.split(line))
            proc.wait()

    def _enable_nginx_firewall_profile(self):
        self.status = MaintenanceStatus("setting up ufw rules...")

        proc = Popen(shlex.split("ufw allow 'Nginx HTTP'"))
        proc.wait()

    def _start_nginx(self, restart: bool = False):
        self.status = MaintenanceStatus("starting nginx...")

        verb = "restart" if restart else "start"
        proc = Popen(shlex.split(f"systemctl {verb} nginx"))
        proc.wait()

    def _reload_nginx(self):
        self.status = MaintenanceStatus("reloading nginx...")

        proc = Popen(shlex.split(f"systemctl reload nginx"))
        proc.wait()

    def _stop_nginx(self):
        self.status = MaintenanceStatus("stopping nginx...")

        proc = Popen(shlex.split(f"systemctl stop nginx"))
        proc.wait()


if __name__ == "__main__":
    ops.main.main(IntroToCharmingMcCharm)
