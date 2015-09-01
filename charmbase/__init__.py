from .model.namespace import dnr

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
    """
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
