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
import subprocess

import ops
from ops import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)

VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class IntroToCharmingMcCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)

    @staticmethod
    def _run_local(*args, **kwargs):
        # to facilitate mocking in test code
        return subprocess.Popen(*args, **kwargs).wait()

    def _on_install(self, event):
        self._install_nginx()  # this will also start it by default
        self._enable_nginx_firewall_profile()
        self.unit.status = ActiveStatus()

    def _install_nginx(self):
        self.unit.status = MaintenanceStatus("installing nginx...")

        script = (
            "apt-get update -y",
            "apt-get install -y nginx",
        )
        for line in script:
            self._run_local(shlex.split(line))

    def _enable_nginx_firewall_profile(self):
        self.unit.status = MaintenanceStatus("setting up ufw rules...")

        self._run_local(shlex.split("ufw allow 'Nginx HTTP'"))

    def _start_nginx(self, restart: bool = False):
        self.unit.status = MaintenanceStatus("starting nginx...")

        verb = "restart" if restart else "start"
        self._run_local(shlex.split(f"systemctl {verb} nginx"))

    def _reload_nginx(self):
        self.unit.status = MaintenanceStatus("reloading nginx...")

        self._run_local(shlex.split("systemctl reload nginx"))

    def _stop_nginx(self):
        self.unit.status = MaintenanceStatus("stopping nginx...")

        self._run_local(shlex.split("systemctl stop nginx"))


if __name__ == "__main__":
    ops.main.main(IntroToCharmingMcCharm)
