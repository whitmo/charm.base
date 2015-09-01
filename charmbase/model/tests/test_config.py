from . import here
from mock import Mock
from mock import call
import json
import pytest


@pytest.fixture(scope="function")
def cmr(request):
    from . import runner_mocks
    r_m = runner_mocks.fixture(request, ns="charmbase.model.config.Config")
    return r_m


@pytest.fixture(scope="function")
def config_ns(cmr):
    from charmbase.model.config import Config
    root = Mock(name='root')
    root.charmdir = here / 'basecharm'
    cfg = Config(root=root)
    return cfg, cmr


def test_config_base(config_ns):
    cfg, cmr = config_ns
    assert cfg.path == here / 'basecharm/config.yaml'
    assert set(cfg.base.keys()) == set(['string-option',
                                        'boolean-option',
                                        'int-option'])


def test_config_defaults(config_ns):
    cfg, cmr = config_ns
    assert cfg.defaults == {'string-option': 'Default Value',
                            'boolean-option': False,
                            'int-option': 9001}


def test_bare_init(cmr):
    from charmbase.model.config import Config
    cfg = Config()
    assert hasattr(cfg, 'get_state')


def test_config_get_state_no_key(config_ns):
    cfg, cmr = config_ns
    mock = cfg.get_state.keywords.get('runner', None)
    mock.return_value = "{}"
    assert cfg.current_raw == {}
    assert cmr.root.get_state.called
    assert cmr.root.get_state.call_args == call(['config-get',
                                                 '--format=json'])


def test_config_get_state_key(config_ns):
    cfg, cmr = config_ns
    mock = cmr.root.get_state
    mock.return_value = json.dumps(1)
    assert cfg.get_state(key='wat') == 1
    assert cmr.root.get_state.called
    assert cmr.root.get_state.call_args == call(['config-get',
                                                 '--format=json', 'wat'])
