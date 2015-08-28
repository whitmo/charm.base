from pytest import fixture

@fixture
def bare_xc():
    from charmbase import execution_context
    return execution_context()




def test_xc_import():
    from charmbase.model import context
    xc = context.ExecutionContext()
