from charmbase.model.namespace import ToolNamespace as tns
from functools import partial
import inspect


class Tooled(tns):
    """
    T1
    """


class Tooled2(tns):
    """
    T2
    """
    @classmethod
    def includeme(cls, obj):
        cls._old_tools = cls._tools.copy()
        for key, cbl in obj._tools.items():
            args = inspect.getargspec(cbl)[0]
            if "sideeffect" in args:
                cls._tools[key] = partial(cbl, sideeffect=lambda: "SAFE")



@Tooled.register_tool('tooly')
def toolin():
    return 1


@Tooled.register_tool
@Tooled2.register_tool
def toolit(sideeffect=lambda:"BOOM"):
    return sideeffect()
