from .context import ExecutionContext
from .tools import ToolNamespace


@ExecutionContext.register_child
class Unit(ToolNamespace):
    """
    Unit information

    unit-get print public-address or private-address
    """
