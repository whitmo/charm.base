from .context import ExecutionContext
from .meta import reify
from .tools import ToolNamespace
import json
import yaml
import subprocess


@ExecutionContext.register_child
class Config(ToolNamespace):
    """
    Represent configuration values and their access
    """

    @reify
    def current_raw(self):
        state = self.get_state()
        state = state and state or {}
        return state

    @reify
    def path(self):
        return self.root.charmdir / 'config.yaml'

    @reify
    def base(self):
        """
        The initial configuration file data
        """
        txt = self.path.text()
        return yaml.load(txt)['options']

    @reify
    def defaults(self):
        return {key: val['default'] for key, val in self.base.items()}


@Config.register_tool('get_state')
def config_get(key=None, command="config-get", runner=subprocess.check_output):
    command = [command]
    command.extend(['--format=json'])
    if key is not None:
        command.append(key)
    out = runner(command)
    return json.loads(out)
