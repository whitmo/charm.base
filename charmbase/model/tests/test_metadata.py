from mock import Mock
from . import here
import pytest


@pytest.fixture(scope="function")
def mdmr(request):
    from . import runner_mocks
    r_m = runner_mocks.fixture(request, ns="charmbase.model.metadata.Metadata")
    return r_m


def test_bare_init(mdmr):
    from charmbase.model.metadata import Metadata
    assert Metadata()


@pytest.fixture(scope="function")
def metadata_ns(mdmr):
    from charmbase.model.metadata import Metadata
    root = Mock(name='root')
    root.charmdir = here / 'basecharm'
    md = Metadata(root=root)
    return md, mdmr


def test_raw_metadata(metadata_ns):
    md, mdmr = metadata_ns
    assert set(md.raw.keys()) == set(['description',
                                      'maintainer',
                                      'name',
                                      'peers',
                                      'provides',
                                      'requires',
                                      'subordinate',
                                      'summary',
                                      'tags'])


def test_metadata_attrs(metadata_ns):
    md, _ = metadata_ns
    assert md.subordinate == False
    iface = {'interface': 'interface-name'}
    assert md.provides == {'provides-relation': iface}
    assert md.requires == {'requires-relation': iface}
    assert md.peers == {'peer-relation': iface}


def test_metadata_attr_missing(metadata_ns):
    md, _ = metadata_ns
    with pytest.raises(AttributeError):
        md.wat
