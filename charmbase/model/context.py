from .namespace import Namespace
from .namespace import dnr
from .meta import registrator

from functools import wraps
from path import path
from tempfile import mkdtemp
import os
import textwrap


"""
declare -x JUJU_AGENT_SOCKET="@/var/lib/juju/agents/unit-ubuntu-0/agent.socket"
declare -x JUJU_API_ADDRESSES="172.31.1.40:17070"
declare -x JUJU_AVAILABILITY_ZONE=""
declare -x JUJU_CHARM_DIR="/var/lib/juju/agents/unit-ubuntu-0/charm"
declare -x JUJU_CONTEXT_ID="ubuntu/0-install-1002841046484389285"
declare -x JUJU_DEBUG="/tmp/tmp.2esNGFMfdX"
declare -x JUJU_ENV_NAME="ec2-va-1"
declare -x JUJU_ENV_UUID="b8ba8824-16f2-43b0-8b10-5b1dfa063906"
declare -x JUJU_HOOK_NAME="install"
declare -x JUJU_MACHINE_ID="2"
declare -x JUJU_METER_INFO=""
declare -x JUJU_METER_STATUS="NOT SET"
declare -x JUJU_UNIT_NAME="ubuntu/0"
"""


class ExecutionContext(Namespace):
    _namespaces = {}
    _default_tool = {}
    _iso_dicts = '_tools',
    environment_keys = textwrap.dedent("""
    JUJU_RELATION
    JUJU_RELATION_ID
    JUJU_UNIT_NAME
    JUJU_REMOTE_UNIT
    JUJU_HOOK_NAME
    JUJU_ACTION_NAME
    JUJU_ACTION_UUID
    JUJU_ACTION_TAG
    """)

    default_modules = """
    charmbase.model.tools
    charmbase.model.relation
    charmbase.model.config
    charmbase.model.metadata
    charmbase.model.unit
    """

    cache = {}

    register_tool = registrator('_tools')

    def __init__(self,
                 environment=None,
                 tools=None,
                 charmdir=None,
                 tempdir=None,
                 rootdir=None,
                 init_dirs=True,
                 base_includes=default_modules.split(),
                 add_includes=None,
                 resolver=dnr):
        self._root = True
        self._parent = None
        self.resolver = resolver
        self._modules = {}
        self.environment = environment or {}
        self._tools = tools or {}

        self.tempdir = tempdir and path(tempdir) or path(mkdtemp(suffix=".charm"))
        self.charmdir = charmdir and path(charmdir) or self.tempdir / 'charm'
        self.rootdir = rootdir and path(rootdir) or self.tempdir / 'root'

        if init_dirs is True:
            self.rootdir.makedirs_p()
            self.charmdir.makedirs_p()

        for key, ns in self._children.items():
            setattr(self, key, ns)

        juju_env = self.filter_map_by_prefix("JUJU_", self.environment)
        self.init_attrs(self, juju_env)
        self.init_attrs(self, self._tools)
        self.load_includes(base_includes)
        self.load_includes(add_includes)
        self.initialize_children()


    @staticmethod
    def filter_map_by_prefix(prefix, map_):
        return {
            key.replace(prefix, ""): val \
            for key, val in map_.items() \
            if key.startswith(prefix)
            }


    @classmethod
    def from_yaml(cls, fp):
        txt = path(fp).text()
        data = yaml.load(txt)
        return cls(**data)

    @classmethod
    def from_environment(cls):
        return cls(environment=os.environ)

    def flush(key):
        """
        Flushes any entries from function cache where the key is found in the
        function+args
        """
        flush_list = []
        for item in self.cache:
            if key in item:
                flush_list.append(item)
        for item in flush_list:
            del self.cache[item]

    def cached(self, func):
        """Cache return values for multiple executions of func + args

        For example::

        @cached
        def unit_get(attribute):
        pass

        unit_get('test')

        will cache the result of unit_get + 'test' for future calls.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = self.cache
            key = str((func, args, kwargs))
            try:
                return cache[key]
            except KeyError:
                pass  # Drop out of the exception handler scope.
            res = func(*args, **kwargs)
            cache[key] = res
            return res
        wrapper._wrapped = func
        return wrapper


@ExecutionContext.register_child
class Env(Namespace):
    """
    Represent the environmental variable unfiltered as attributes
    """
    def __init__(self, root=None, parent=None, resolver=None, includes=None):
        super(Env, self).__init__(root, parent, resolver=resolver, includes=includes)
        self.init_attrs(self, self._root.environment)


class DuplicateNamespaceError(RuntimeError):
    """
    Duplicate namespace error
    """


class DuplicateDefaultToolError(RuntimeError):
    """
    Duplicate default tool error
    """
