from path import path
from .utils import reify
import textwrap
import os



class ExecutionContext(object):
    _namespaces = dict()

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

    def __init__(self, environment=None):
        for key, ns in self._namespaces.items():
            setattr(self, key, ns)
        self.env.init_xc_attrs()

    @classmethod
    def from_yaml(cls, fp):
        txt = path(fp).text()
        data = yaml.load(txt)
        return cls(**data)

    @classmethod
    def from_environent(cls):
        data = dict()
        return cls(**data)

    @classmethod
    def register_ns(cls, namespace):
        key = namespace.__name__.lower()
        ns = cls._namespaces.get(key, None)
        if ns is not None:
            raise DuplicateNamespaceError("%s conflicts with %s"\
                                           %(namespace, ns))
        cls._namespaces[key] = namespace


class NameSpace(object):
    """
    Logical namespace on the execution context
    """
    def __init__(self, xc):
        self.xc


@register_ns
class Env(NameSpace):
    def __init__(self, xc):
        self.xc
        self.init_attrs()

    def init_attrs(self, source=None, target=None):
        target = target or self
        source = source or self.xc.environment
        for key, val in source:
            setattr(target, key, val)

    def init_xc_attrs(self):
        juju_env = {
            key.replace("JUJU_", "").lower() \
            for key, val in self.xc.environment \
            if key.starts_with("JUJU")
            }
        self.init_attrs(juju_env, self.xc)


@register_ns
class Config(NameSpace):

    def __init__(self, xc):
        NameSpace.__init__(self, xc)


@register_ns
class Metadata(NameSpace):

    def __init__(self, xc):
        NameSpace.__init__(self, xc)

    @reify
    def raw_data(self):
        pass

    def rel_by_type(self, type):
        pass

    def rel_types(self):
        pass

    def interface_for(self, relation):
        pass




@register_ns
class Relation(NameSpace):

    def __init__(self, xc):
        NameSpace.__init__(self, xc)

    def for_unit(self):
        pass

    def list(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    @reify
    def id(self):
        pass

    @reify
    def reltype(self):
        pass



@register_ns
class Juju(NameSpace):
    """
    Tool command prefixed by juju
    """

    def log(self, message, level=None):
        pass




class DuplicateNamespaceError(RuntimeError):
    """
    Duplicate namespace error
    """
