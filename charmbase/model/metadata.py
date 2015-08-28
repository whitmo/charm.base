from .context import ExecutionContext
from .namespace import Namespace


@ExecutionContext.register_child
class Metadata(Namespace):

    def raw_data(self):
        pass

    def rel_by_type(self, type):
        pass

    def rel_types(self):
        pass

    def interface_for(self, relation):
        pass
