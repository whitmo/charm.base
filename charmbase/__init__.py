from .model.namespace import dnr
from path import path


def execution_context(environment=None,
                      tools=None,
                      charmdir=None,
                      tempdir=None,
                      rootdir=None,
                      init_dirs=True,
                      base_includes=None,
                      add_includes=None,
                      override_includes=None):
    """
    A convenience function for initializing an execution context

    If `environment` is None, os.environ will be used. Subsequently if
    `charmdir` is not set, os.environ['JUJU_CHARM_DIR'] substitute and
    if if `rootdir` is not set, it will be "/".
    """
    if environment is None:
        import os
        environment = os.environ
        if charmdir is None:
            charmdir = os.environ.get('JUJU_CHARM_DIR', None)
        if rootdir is None:
            rootdir = path("/")

    xc = dnr.resolve("charmbase.model.context.ExecutionContext")
    base_includes = base_includes or xc._default_modules
    return xc(environment,
              tools,
              charmdir,
              tempdir,
              rootdir,
              init_dirs,
              base_includes,
              add_includes,
              override_includes)
