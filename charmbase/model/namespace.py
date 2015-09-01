"""
A bag of pointers
"""
from .meta import IsolatedDicts
from .meta import registrator
from .meta import dnr
from textwrap import dedent
from logging import getLogger

logger = getLogger(__name__)


class Namespace(object):
    """
    Logical namespace on the execution context
    """
    __metaclass__ = IsolatedDicts
    _iso_dicts = '_children', '_includes',

    def __init__(self, root=None, parent=None, resolver=dnr, includes=None):
        self.root = self._root = root is not None and root or True
        self._parent = parent
        self.resolver = dnr
        self.initialize_children()
        self.load_includes(includes)

    @staticmethod
    def init_attrs(target, source):
        for key, val in source.items():
            setattr(target, key, val)

    @staticmethod
    def filter_map_by_prefix(prefix, map_in):
        map_out = {
            key.replace(prefix, "").lower(): val \
            for key, val in map_in.items() \
            if key.startswith(prefix)
            }
        return map_out

    class DuplicateNamespaceError(RuntimeError):
        """
        Duplicate namespace error
        """

    register_child = registrator.factory('_children',
                                         error=DuplicateNamespaceError)

    def initialize_children(self):
        root = self._root is True and self or self._root
        parent = self
        if self._children:
            for name, nsctor in self._children.items():
                if not hasattr(self, name):
                    setattr(self, name, nsctor(root, parent, self.resolver))

    def yield_callable(self, candidate):
        includeme = getattr(candidate, 'includeme', None)
        if callable(includeme):
            yield includeme

        if callable(candidate):
            yield candidate

        yield False

    def load_includes(self, specs):
        specs = isinstance(specs, basestring) \
            and dedent(specs).split() or specs

        specs = specs and [x for x in specs if x] or []

        for spec in specs:
            if spec not in self._includes:
                obj = self.resolver.resolve(spec)
                self._includes[spec] = obj
                includeme = next(self.yield_callable(obj))
                if not (includeme is False):
                    includeme(self)
                else:
                    logger.warn("%s return a non-callable obj: %s", spec, obj)


class ToolNamespace(Namespace):
    _iso_dicts = '_tools',

    def __init__(self, root=None, parent=None, resolver=dnr, includes=None):
        super(ToolNamespace, self).__init__(root, parent,
                                            resolver=resolver,
                                            includes=includes)
        self.init_attrs(self, self._tools)

    class DuplicateDefaultToolError(RuntimeError):
        """
        Duplicate default tool error
        """

    register_tool = registrator.factory('_tools',
                                        error=DuplicateDefaultToolError)
