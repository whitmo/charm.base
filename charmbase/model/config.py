from .context import ExecutionContext
from .tools import ToolNamespace


@ExecutionContext.register_child
class Config(ToolNamespace):
    """
    Represent configuration values and their access
    """
