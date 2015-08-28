from functools import partial
from logging import getLogger

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


def register_resource(cls, resource, registry_name=None):
    registry = getattr(cls, registry_name)
    #reg2 = getattr(resource, registry_name, None)
    key = resource.__name__.lower()
    ns = registry.get(key, None)
    if ns is not None:
        raise DuplicateNamespaceError("%s conflicts with %s" \
                                      % (resource, ns))
    registry[key] = resource
    setattr(cls, registry_name, registry)
    return resource


def registrator(name):
    return classmethod(partial(register_resource, registry_name=name))


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
