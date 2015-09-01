from .meta import dnr
from .meta import reify
from .namespace import Namespace
from .namespace import ToolNamespace
from functools import wraps
from path import path
from tempfile import mkdtemp
import textwrap


class ExecutionContext(ToolNamespace):
    _namespaces = {}
    _default_tool = {}
    _iso_dicts = '_tools',
    _environment_keys = textwrap.dedent("""
    JUJU_RELATION
    JUJU_RELATION_ID
    JUJU_UNIT_NAME
    JUJU_REMOTE_UNIT
    JUJU_HOOK_NAME
    JUJU_ACTION_NAME
    JUJU_ACTION_UUID
    JUJU_ACTION_TAG
    """)

    _default_modules = """
    charmbase.model.tools
    charmbase.model.relation
    charmbase.model.config
    charmbase.model.metadata
    charmbase.model.unit
    """

    cache = {}

    def __init__(self,
                 environment=None,
                 tools=None,
                 charmdir=None,
                 tempdir=None,
                 rootdir=None,
                 init_dirs=True,
                 base_includes=_default_modules,
                 add_includes=None,
                 override_includes=None,
                 resolver=dnr):

        self._root = True
        self._parent = None
        self.resolver = resolver
        self._modules = {}
        self.environment = environment or {}
        self._tools = tools or {}

        juju_env = self.filter_map_by_prefix("JUJU_", self.environment)
        self.init_attrs(self, juju_env)

        self.tempdir = tempdir and path(tempdir) \
            or path(mkdtemp(suffix=".charm"))

        self.charmdir = charmdir and path(charmdir) or self.tempdir / 'charm'
        self.rootdir = rootdir and path(rootdir) or self.tempdir / 'root'

        if init_dirs is True:
            self.rootdir.makedirs_p()
            self.charmdir.makedirs_p()

        self.init_attrs(self, self._tools)
        self.load_includes(base_includes)
        self.load_includes(add_includes)
        self.initialize_children()
        self.load_includes(override_includes)

    @reify
    def charm_name(self):
        return self.metadata.name

    @reify
    def service_name(self):
        return self.unit_name.split('/')[0]

    @classmethod
    def from_environment(cls, add_includes=None, override_includes=None):
        import os
        charmdir = path(os.environ['JUJU_CHARM_DIR'])
        return cls(environment=os.environ,
                   charmdir=charmdir,
                   rootdir=path("/"),
                   add_includes=add_includes,
                   override_includes=override_includes)

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
    def __init__(self, root=None, parent=None,
                 resolver=None, includes=None):
        super(Env, self).__init__(root, parent,
                                  resolver=resolver, includes=includes)
        self.init_attrs(self, self._root.environment)
