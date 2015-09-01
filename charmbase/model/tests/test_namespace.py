from unittest import TestCase
import pytest


def test_class_dict_creation():
    import nsex
    assert hasattr(nsex.T1NS, '_children')
    assert hasattr(nsex.T2NS, '_children')
    assert not(nsex.T1NS._children is nsex.T2NS._children)
    assert hasattr(nsex.T1NS, 'wat')


def test_parenting():
    import nsex
    assert 't2ns' in nsex.T1NS._children
    assert nsex.T2NS in nsex.T1NS._children.values()
    ns = nsex.T1NS()
    assert hasattr(ns, 't2ns')
    assert hasattr(ns.t2ns, 't3ns')



def test_overriding_with_implicit_include(clean_up_tools):
    """
    Really a namespace test
    """
    import tnsex
    tns = tnsex.Tooled2(includes="charmbase.model.tests.tnsex.Tooled2")
    assert tns.toolit() == "SAFE"


def test_overriding_with_explicit_include(clean_up_tools):
    """
    Really a namespace test
    """
    import tnsex
    tns = tnsex.Tooled2(includes="charmbase.model.tests."
                        "tnsex.Tooled2.includeme")
    assert tns.toolit() == "SAFE"






def test_toolnamespace():
    import tnsex
    t = tnsex.Tooled()
    assert hasattr(t, 'tooly')
    assert t.tooly() == 1
    assert hasattr(t, 'toolit')
    assert t.toolit() == "BOOM"


def test_include_loading():
    import nsex
    ns = nsex.T1NS(includes="charmbase.model.tests.nsex")
    assert ns.hello == 'included'


@pytest.fixture(scope="function")
def clean_up_tools(request):
    import tnsex

    def clear_tools():
        for cls in tnsex.Tooled2,:
            cls._tools = cls._old_tools

    request.addfinalizer(clear_tools)




def test_toolnamespace_tool_init():
    pass



class TestNSBase(TestCase):
    def makeone(self, root=None, parent=None, resolver=None):
        from charmbase.model import namespace as mod
        return mod.Namespace(root, parent, resolver)

    def test_init(self):
        ns = self.makeone()
        assert ns._root is True
        assert ns._parent is None
