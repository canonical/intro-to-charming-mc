"""Demo library to offer demo ingress integrations for intro-to-charming-mc nginx charm.
"""
import logging
import socket
from typing import List, Tuple

import ops

logger = logging.getLogger(__name__)

# The unique Charmhub library identifier, never change it
LIBID = "4e46e1e7f79f4164a9d21dd79e354ff0"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1

DEFAULT_ENDPOINT = "ingress_demo"


class IngressProvider:
    def __init__(self, charm: ops.CharmBase, endpoint_name: str = DEFAULT_ENDPOINT):
        self._charm = charm
        self._endpoint_name = endpoint_name

    @property
    def relations(self) -> List[ops.Relation]:
        return self._charm.model.relations[self._endpoint_name]

    def requests(self) -> List[Tuple[str, int]]:
        reqs = []

        for relation in self.relations:
            if not relation.app or not relation.data:
                logger.debug(f"relation {relation} not ready: no app")
                continue

            app_data = relation.data[relation.app]

            if not app_data:
                logger.debug(f"relation {relation} not ready: remote did not request() yet")
                continue

            try:
                port = int(app_data['port'])
                host = app_data['host']
            except (TypeError, KeyError):
                logger.error(f"failed validating databag contents for {relation}", exc_info=True)
                continue

            reqs.append((host, port))

        return reqs


class IngressRequirer:
    def __init__(self, charm: ops.CharmBase, endpoint_name: str = DEFAULT_ENDPOINT):
        self._charm = charm
        self._endpoint_name = endpoint_name

    @property
    def relation(self) -> ops.Relation:
        return self._charm.model.get_relation(self._endpoint_name)

    def request(self, port: int, host: str = None):
        host = host or socket.getfqdn()
        self.relation.data[self._charm.app]['port'] = str(port)
        self.relation.data[self._charm.app]['host'] = str(host)
