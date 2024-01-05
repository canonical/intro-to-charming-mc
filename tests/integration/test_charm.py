#!/usr/bin/env python3
# Copyright 2024 pietro
# See LICENSE file for licensing details.

import asyncio
import logging
import os
import shutil
from pathlib import Path

import pytest
import yaml
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

METADATA = yaml.safe_load(Path("./charmcraft.yaml").read_text())
APP_NAME = METADATA["name"]


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    """Build the charm-under-test and deploy it together with related charms.

    Assert on the unit status before any relations/configurations take place.
    """
    # Build and deploy charm from local source folder
    charm = await ops_test.build_charm(".")

    # Deploy the charm and wait for active/idle status
    await asyncio.gather(
        ops_test.model.deploy(charm, application_name=APP_NAME),
        ops_test.model.wait_for_idle(
            apps=[APP_NAME], status="active", raise_on_blocked=True, timeout=1000
        ),
    )


@pytest.fixture(scope="module", autouse=True)
def copy_lib_into_tester_charm(ops_test):
    # ensure tester copy is up-to-date if we make changes to the base lib
    lib = "intro_to_charming_mc/v0/demo_ingress.py"
    install_path = f"tests/integration/tester/lib/charms/{lib}"
    os.makedirs(os.path.dirname(install_path), exist_ok=True)
    shutil.copyfile(f"lib/charms/{lib}", install_path)
