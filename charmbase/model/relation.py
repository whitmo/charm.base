from .context import ExecutionContext
from .tools import ToolNamespace


@ExecutionContext.register_child
class Relation(ToolNamespace):
    """
    Tool commands prefixed by `relation-`

    relation-get   get relation settings
    relation-ids   list all relation ids with the given relation name
    relation-list  list relation units
    relation-set   set relation settings
    """

    def for_unit(self):
        pass

    def list(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    def id(self):
        pass

    def reltype(self):
        pass
