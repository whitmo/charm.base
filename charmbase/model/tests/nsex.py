from charmbase.model import dnr

ns = dnr.resolve('charmbase.model.namespace.Namespace')


def includeme(ns):
    ns.hello = "included"
    return ns


class T1NS(ns):
    """
    T1
    """
    _iso_dicts = ['wat', 'hey']


@T1NS.register_child
class T2NS(ns):
    """
    T2
    """


@T2NS.register_child
class T3NS(T2NS):
    """
    inherits from t2
    """
