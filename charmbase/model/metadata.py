from . import dnr
from .context import ExecutionContext
from .meta import reify
from .namespace import Namespace
import yaml


@ExecutionContext.register_child
class Metadata(Namespace):

    def __init__(self, root=None, parent=None, resolver=dnr, includes=None):
        super(Metadata, self).__init__(root, parent,
                                       resolver=resolver,
                                       includes=includes)
        if self.root and self.root is not True:
            self.init_attrs(self, self.raw)

    @reify
    def raw(self):
        md = self.root.charmdir / 'metadata.yaml'
        raw = md.text()
        return yaml.load(raw)

    def rel_by_type(self, type):
        pass

    def rel_types(self):
        pass

    def interface_for(self, relation):
        pass
