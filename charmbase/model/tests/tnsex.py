from charmbase.model.namespace import ToolNamespace as tns


class Tooled(tns):
    """
    T1
    """


@Tooled.register_tool
def toolin():
    return 1
