from .context import ExecutionContext as ctx
from .namespace import ToolNamespace
import subprocess

"""
odd ballz

add-metric     send metrics
config-get     print service configuration
unit-get       print public-address or private-address
"""


@ctx.register_tool
def owner_get(setting='tag', command="owner-get", runner=subprocess.call):
    """
    owner-get      print information about the owner of the service. The only valid value for <setting> is currently tag
    """
    command = [command]
    command.append(setting)
    runner(command)


@ctx.register_child
class Juju(ToolNamespace):
    """
    Tool commands prefixed by `juju-`

    juju-log       write a message to the juju log
    juju-reboot    Reboot the host machine
    """


@Juju.register_tool('log')
def juju_log(message, level=None, command="juju-log", runner=subprocess.call):
    command = [command]
    if level:
        command += ['-l', level]
    if not isinstance(message, six.string_types):
        message = repr(message)
    command += [message]
    return runner(command)


@Juju.register_tool('reboot')
def juju_reboot(now=False, runner=subprocess.call, command='juju-reboot'):
    now and commmand.append("--now")
    runner(command)


@ctx.register_child
class Action(ToolNamespace):
    """
    Tool commands prefixed by `action-`

    action-fail    set action fail status with message
    action-get     get action parameters
    action-set     set action results
    """

@ctx.register_child
class Port(ToolNamespace):
    """
    Tool commands related to ports

    close-port     ensure a port or range is always closed
    open-port      register a port or range to open
    opened-ports   lists all ports or ranges opened by the unit
    """

@ctx.register_child
class Status(ToolNamespace):
    """
    Tool commands prefixed by `status-`

    status-get
    status-set
    """

@ctx.register_child
class Storage(ToolNamespace):
    """
    Tool commands prefixed by `storage-`

    storage-add
    storage-get
    """

@ctx.register_child
class Leader(ToolNamespace):
    """
    Tool commands dealing with leader election

    is-leader
    leader-get
    leader-set
    """
