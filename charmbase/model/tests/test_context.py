from pytest import fixture


def test_initialize_convenience_function(bare_xc):
    from charmbase import execution_context
    xc = execution_context()
    assert xc


def test_xc_import():
    from charmbase.model import context
    xc = context.ExecutionContext()


def test_environment_setting():
    from charmbase import execution_context
    xc = execution_context(environment=dict(hey="wat", JUJU_STUFF="yeah"))
    assert xc.stuff == "yeah"
    assert xc.env.hey == "wat"
