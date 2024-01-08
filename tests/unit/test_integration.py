import ops
from charms.intro_to_charming_mc.v0.demo_ingress import IngressProvider, IngressRequirer
from ops import Framework
from scenario import Context, Relation, State


class MyRequirerCharm(ops.CharmBase):
    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.require_ingress = IngressRequirer(self)

        framework.observe(self.on.update_status, self._on_update_status)

    def _on_update_status(self, _e):
        self.require_ingress.request(42, "foo.com")


def test_requirer_request():
    ctx = Context(
        MyRequirerCharm,
        meta={"name": "mycharm", "provides": {"demo-ingress": {"interface": "demo_ingress"}}},
    )
    state_in = State(leader=True, relations=[Relation("demo-ingress")])

    state_out = ctx.run("update_status", state_in)

    local_app_data = state_out.get_relations("demo-ingress")[0].local_app_data
    assert local_app_data == {"host": "foo.com", "port": "42"}


class MyProviderCharm(ops.CharmBase):
    def __init__(self, framework: Framework):
        super().__init__(framework)
        self.provide_ingress = IngressProvider(self)

        framework.observe(self.on.update_status, self._on_update_status)

    def _on_update_status(self, _e):
        for relation, args in self.provide_ingress.requests():
            self.provide_ingress.respond(relation, "http://www.example.com")
            self._received_args = args


def test_requirer_accept():
    ctx = Context(
        MyProviderCharm,
        meta={"name": "mycharm", "requires": {"demo-ingress": {"interface": "demo_ingress"}}},
    )
    state_in = State(
        leader=True,
        relations=[Relation("demo-ingress", remote_app_data={"host": "foo.com", "port": "42"})],
    )

    with ctx.manager("update_status", state_in) as mgr:
        mgr.run()
        assert mgr.charm._received_args == ("foo.com", 42)

    relation = mgr.output.get_relations("demo-ingress")[0]
    assert relation.local_app_data == {"url": "http://www.example.com"}
