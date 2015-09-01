from functools import partial
from logging import getLogger
from dotted_name_resolver import DottedNameResolver

dnr = DottedNameResolver()
logger = getLogger(__name__)


class IsolatedDicts(type):
    """
    Creates a unique dictionaries any name in cls._iso_dicts as a class
    vars for every subclass.

    Walks bases to inherit inherit names but not maps.
    """
    @staticmethod
    def chain(dct, bases, attr):
        for attrname in dct.get(attr, []):
            yield attrname

        for base in bases:
            for cls in base.mro():
                map_list = getattr(cls, attr, False)
                if not(map_list is False):
                    for attrname in map_list:
                        yield attrname

    def __new__(meta, name, bases, dct):
        for attrname in meta.chain(dct, bases, '_iso_dicts'):
            d = dct[attrname] = {}
        return super(IsolatedDicts, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):

        super(IsolatedDicts, cls).__init__(name, bases, dct)


class registrator(object):

    def __init__(self, registry_name=None, error=None, resolver=dnr):
        self.registry_name = registry_name
        self.error = error
        self.resolve = dnr.maybe_resolve

    def _register_resource(self, cls, resource, name=None):
        registry = getattr(cls, self.registry_name)
        key = name and name or resource.__name__.lower()
        regged_resource = registry.get(key, None)
        if regged_resource is not None:
            raise self.error("%s conflicts with %s"
                             % (resource, regged_resource))
        registry[key] = resource
        setattr(cls, self.registry_name, registry)

    def maybe_load(self, name):
        if name.find('.') == -1:
            return None

    def register_resource(self, cls, resource=None, name=None):
        if isinstance(resource, basestring):
            if not resource.find('.') == -1:
                loaded = self.resolve(resource)
                if loaded is not None:
                    self._register_resource(cls, resource, name)
                    return resource
                else:
                    logger.warn("%s does not resolve to python path, "
                                "treating as a resource name", resource)

            return partial(self.register_resource, cls, name=resource)
        self._register_resource(cls, resource, name)
        return resource

    @classmethod
    def factory(cls, name, error=Exception):
        regger = cls(name, error)

        @classmethod
        def registrator(cls, resource=None, name=None, reg=regger):
            return reg.register_resource(cls, resource, name)

        return registrator


# from pyramid
class reify(object):
    """ Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.  An example:

    .. code-block:: python

       class Foo(object):
           @reify
           def jammy(self):
               print('jammy called')
               return 1

    And usage of Foo:

    >>> f = Foo()
    >>> v = f.jammy
    'jammy called'
    >>> print(v)
    1
    >>> f.jammy
    1
    >>> # jammy func not called the second time; it replaced itself with 1
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except: # pragma: no cover
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val
