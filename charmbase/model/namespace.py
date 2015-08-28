"""
A bag of pointers
"""
from dotted_name_resolver import DottedNameResolver
from functools import partial
from .meta import IsolatedDicts
from .meta import registrator
from textwrap import dedent
from pprint import pprint as pp
dnr = DottedNameResolver()


class Namespace(object):
    """
    Logical namespace on the execution context
    """
    __metaclass__ = IsolatedDicts
    _iso_dicts = '_children', '_includes',

    def __init__(self, root=None, parent=None, resolver=dnr, includes=None):
        self._root = root is not None and root or True
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

    register_child = registrator('_children')

    def initialize_children(self):
        root = self._root is True and self or self._root
        parent = self
        if self._children:
            for name, nsctor in self._children.items():
                if not hasattr(self, name):
                    setattr(self, name, nsctor(root, parent, self.resolver))

    def load_includes(self, specs):
        specs = isinstance(specs, basestring) \
            and dedent(specs).split() or specs

        specs = specs and [x for x in specs if x] or []

        for spec in specs:
            if not spec in self._includes:
                obj = self.resolver.resolve(spec)
                self._includes[spec] = obj
                includeme = getattr(obj, 'includeme', False)
                if not (includeme is False):
                    includeme(self)


class ToolNamespace(Namespace):
    _iso_dicts = '_tools',

    def __init__(self, root=None, parent=None, resolver=dnr, includes=None):
        super(ToolNamespace, self).__init__(root, parent, resolver=resolver, includes=includes)
        self.init_attrs(self, self._tools)

    register_tool = registrator('_tools')
