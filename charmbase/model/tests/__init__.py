from ..meta import dnr
from functools import partial
from mock import Mock
from path import path
from stuf import stuf


here = path(__file__).parent


class runner_mocks(stuf):
    current_run = None

    def __init__(self):
        self.mocks = stuf()

    @classmethod
    def fixture(cls, request, ns=None):
        ns = dnr.resolve(ns)
        r_m = cls()
        r_m.mock_all(ns)

        def clear_tool_mocks():
            r_m.clear_all(ns)

        request.addfinalizer(clear_tool_mocks)
        return r_m

    def mock_ns_tools(self, ns, ns_name, tools):
        ns._original_tools = tools.copy()
        for name, cbl in tools.items():
            mock_name = "%s.%s" % (ns_name, name)
            cls_s = self.setdefault(ns_name, stuf())
            rmock = cls_s[name] = Mock(name=mock_name)
            tools[name] = partial(cbl, runner=rmock)
        return tools

    def clear_ns(self, ns):
        ns._tools = ns._original_tools
        del ns._original_tools

    def clear_all(self, ns):
        self.clear_ns(ns)
        for childname in ns._children.keys():
            child = getattr(ns, childname)
            self.clear_all(child)

    def mock_all(self, ns, name=None):
        name = name and name or "root"
        self.mock_ns_tools(ns, name, getattr(ns, '_tools', {}))
        for childname in ns._children.keys():
            child = getattr(ns, childname)
            self.mock_all(child, childname)

    @classmethod
    def includeme(cls, ns):
        cls.current_run = mock_reg = cls()
        mock_reg.mock_all(ns)
        ns.runner_mocks = mock_reg
        ns.runner_mock_cleanup = partial(mock_reg.clear_all, ns)

    @classmethod
    def clear(cls, ns):
        cls.current_run = None
