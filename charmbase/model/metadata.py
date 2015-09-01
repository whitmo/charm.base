from . import dnr
from .context import ExecutionContext
from .meta import reify
from .namespace import Namespace
import yaml


@ExecutionContext.register_child
class Metadata(Namespace):
    sentinel = object()

    def __init__(self, root=None, parent=None, resolver=dnr, includes=None):
        super(Metadata, self).__init__(root, parent,
                                       resolver=resolver,
                                       includes=includes)

    def __getattr__(self, name):
        val = self.raw.get(name, self.sentinel)
        if val is not self.sentinel:
            return val
        raise AttributeError

    @reify
    def raw(self):
        md = self.root.charmdir / 'metadata.yaml'
        raw = md.text()
        return yaml.load(raw)
