#!/usr/bin/env python3
# Copyright 2024 pietro
# See LICENSE file for licensing details.

"""Charm the application."""

import logging

import ops
from charms.intro_to_charming_mc.v0.demo_ingress import IngressRequirer

logger = logging.getLogger(__name__)


class IntroToCharmingMcTesterCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.ingress_requirer = IngressRequirer(self)
        for event in self.on.events().values():
            self.framework.observe(event, self._on_event)

    def _on_event(self, _event: ops.EventBase):
        ingress = self.ingress_requirer
        if ingress.relation:
            if not (response := ingress.response):
                ingress.request(4242, "this.cluster.local.svc.whatever")
                self.unit.status = ops.WaitingStatus("requested ingress, awaiting response")
            else:
                self.unit.status = ops.ActiveStatus(f"ingress ready at {response}")
        else:
            self.unit.status = ops.BlockedStatus(
                "awaiting relation with demo-ingress-provider charm"
            )


if __name__ == "__main__":  # pragma: nocover
    ops.main.main(IntroToCharmingMcTesterCharm)
