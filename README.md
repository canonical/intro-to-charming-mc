# Intro to Charming Masterclass charm

This is a demo charm developed for a Canonical Masterclass in January 2024. It deploys `nginx` on machine substrates. The operation capability is basically nihil.

☢⚠ **This is not a production charm!** ⚠☢

## Repository instructions

The repository contains 4 branches:

- `part-1-basic-setup`
- `part-2-integrations`
- `part-3-observability`

Each branch corresponds to a hour-long masterclass section and is designed so that, if you're lagging behind a section and the masterclass is moving on to the next, you can check out the corresponding branch and not be left behind.

Each branch/sections covers a selection of core charming topics.

### Prerequisites

- [Juju](https://juju.is/docs/juju/install-juju)
- Access to a machine controller
- [Jhack](https://github.com/canonical/jhack)

### `part-1-basic-setup`

Topics:
- `charmcraft init` and setting up a charm repository and development environment
- what is a charm? https://discourse.charmhub.io/t/talking-to-a-workload-control-flow-from-a-to-z/6161
- the observer pattern and events: https://discourse.charmhub.io/t/charm-lifecycle/5938
- writing and manipulating `charm.py`
- workload installation
- charm status management
- scenario testing for charm status and workload management


### `part-2-integrations`

Topics:
- [`charmcraft create-lib`](https://juju.is/docs/sdk/charmcraft-create-lib) and charm lib creation 
- `charmcraft.yaml` and metadata editing
- intro to provider/requirer relation wrapper pattern
- tester charms for integration testing
- scenario testing for relation code


### `part-3-observability`

Topics:
- working with [`grafana-agent-operator`](https://github.com/canonical/grafana-agent-operator/)
- alert rules, dashboards, and grafana agent library API
- verification: pack, deploy, CMR, observe!

### `part-4-production`

This part does not have a corresponding branch as it is not as code-heavy as the others.

Topics:
- [style guide](https://juju.is/docs/sdk/styleguide)
- [charm maturity framework](https://juju.is/docs/sdk/charm-maturity)
- charmhub listing and documentation
- CI and automated testing
  - [canonical observability workflows](https://github.com/canonical/observability/tree/main/.github/workflows)
  - [canonical data platform workflows](https://github.com/canonical/data-platform-workflows)
- debugging, developing, troubleshooting


Some information I forgot to add to the readme.