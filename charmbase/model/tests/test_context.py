from . import here
import mock
import pytest


def test_initialize_convenience_function():
    from charmbase import execution_context
    xc = execution_context()
    import os
    assert xc.environment is os.environ
    assert str(xc.rootdir) == "/"


def test_xc_import():
    from charmbase.model import context
    xc = context.ExecutionContext(charmdir=here/"basecharm")
    assert xc.juju
    assert xc.config
    assert xc.relation
    assert xc.metadata


def test_environment_setting():
    from charmbase import execution_context
    xc = execution_context(environment=dict(hey="wat", JUJU_STUFF="yeah"), charmdir=here/"basecharm")
    assert xc.stuff == "yeah"
    assert xc.env.hey == "wat"


@pytest.fixture(scope='module')
def fake_env():
    return dict(
        JUJU_AGENT_SOCKET="@/var/lib/juju/agents/unit-test-0/agent.socket",
        JUJU_API_ADDRESSES="172.31.1.40:17070",
        JUJU_AVAILABILITY_ZONE="",
        JUJU_CHARM_DIR=here/'basecharm',
        JUJU_CONTEXT_ID="test/0-install-1002841046484389285",
        JUJU_DEBUG="/tmp/tmp.2esNGFMfdX",
        JUJU_ENV_NAME="ec2-va-1",
        JUJU_ENV_UUID="b8ba8824-16f2-43b0-8b10-5b1dfa063906",
        JUJU_HOOK_NAME="install",
        JUJU_MACHINE_ID="1",
        JUJU_METER_INFO="",
        JUJU_METER_STATUS="NOT SET",
        JUJU_UNIT_NAME="test/0")


def test_environment_full(fake_env):
    from charmbase import execution_context
    xc = execution_context(environment=fake_env, charmdir=here/"basecharm")
    assert xc.charmdir == here/"basecharm"
    assert xc.hook_name == "install"
    assert xc.machine_id == "1"
    assert xc.unit_name == "test/0"
    assert xc.service_name == "test"
    assert xc.charm_name == xc.metadata.name == "basecharm"


def test_from_environment_factory(fake_env):
    with mock.patch("os.environ", new=fake_env):
        from charmbase.model import context
        xc = context.ExecutionContext.from_environment()
        assert xc.charmdir == here/"basecharm"
