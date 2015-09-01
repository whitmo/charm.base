=============
 charms.base
=============

Motivation
==========

`charmhelpers.core.hookenv` is a servicable organically grown
library/framework for doing charming.  Using it and charming in
general, I've desired to improve it in a few ways:

 - create a single entry point to interacting with live hook execution
   environment.

 - Have a syntonic environment I can explore and discover more about
   the possibilities of what I can do in charm.

 - Have an easy way to write tests without unexpected sideeffects.

 - Have a charming system that is naturally easy to extend to fit
   different usecases

Side effects (when you want them)
---------------------------------

Charms currently require 3 forms of interaction with their
environment: filesystem, environmental variable, and jujud based
tools.  Charmer may add more subproccess or system calls atop these
basic dependencies, but charm.base aims to make it easy to avoid
sideeffects for testing and development outside of the context of a
charm.

Basic API
=========

The entry point to the charm is the **execution context**.

Simple Creation
~~~~~~~~~~~~~~~

Here's how to get a basic one to play with::

    >>> from charmbase import execution_context
    >>> from charmbase.model.tests import here
    >>> fake_env = dict(
    ...     JUJU_AGENT_SOCKET="@/var/lib/juju/agents/unit-test-0/agent.socket",
    ...     JUJU_API_ADDRESSES="172.31.1.40:17070",
    ...     JUJU_AVAILABILITY_ZONE="",
    ...     JUJU_CHARM_DIR='ignore',
    ...     JUJU_CONTEXT_ID="test/0-install-1002841046484389285",
    ...     JUJU_DEBUG="/tmp/tmp.2esNGFMfdX",
    ...     JUJU_ENV_NAME="ec2-va-1",
    ...     JUJU_ENV_UUID="b8ba8824-16f2-43b0-8b10-5b1dfa063906",
    ...     JUJU_HOOK_NAME="install",
    ...     JUJU_MACHINE_ID="1",
    ...     JUJU_METER_INFO="",
    ...     JUJU_METER_STATUS="NOT SET",
    ...     JUJU_UNIT_NAME="test/0")
    >>> xc = execution_context(environment=fake_env, charmdir=here / 'basecharm')

The execution context provides direct access to any `JUJU` prefixed
environmental variables:

    >>> xc.hook_name
    'install'

    >>> xc.machine_id
    '1'

As well as conveniences derived from these vars:

    >>> xc.service_name
    'test'

Filesystem isolation and manipulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The creation of the exection context allows for us to pass in a
charmdir and rootdir (or it will use a temporary directory for both as
a convenience)::

    >>> xc.charmdir.name
    Path(u'basecharm')

    >>> xc.rootdir.startswith('/tmp')
    True

This allows for non-destructive testing of filesystem operations such
as adding and remove files in `/etc`.

Both of these are path objects, giving easy access to a variety of
operations common to charming
::

    >>> sorted([str(x.name) for x in xc.charmdir.files()])
    ['README.example', 'config.yaml', 'icon.svg', 'metadata.yaml']

    >>> from pprint import pprint as pp
    >>> print (xc.charmdir / 'metadata.yaml').text()
    name: basecharm
    summary: <Fill in summary here>
    ...


Extension and inversion of control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The execution context is a root node of a simple tree data
structure. While a number of attributes are exposed as a convenience
to the root node, the root also serves as a reference to other
namespaces as a way of logical organizing charming tasks.

Namespaces are registered roughly around files concerns or tools:
config, metadata, juju (log and reboot), relation, unit, leader,
storage, status. Tool namespace may register specific functions that
wrap jujud calls, and if they implement the function signature
correctly, they may be automatically mocked.

Let's demonstrate a simple example.  We'll add `leader_yolo` to our
leader namespace::

    >>> from charmbase.model.tools import Leader
    >>> import subprocess
    >>> @Leader.register_tool("leader_yolo")
    ... def is_leader(command="is-leader", runner=subprocess.check_output):
    ...     return runner([command])

Now, we will load our execution environment with an argument
`add_includes`.  This argument loads a special callable that will
replace all of our tools runners (ie subprocess calls) with mock
objects.
::

    >>> xc = execution_context(environment=fake_env,
    ...                        charmdir=here / 'basecharm',
    ...                        override_includes="charmbase.model.tests.runner_mocks")

We can now manipulate the output of the new tool:

    >>> xc.runner_mocks.leader.leader_yolo.return_value = "YOLO"
    >>> xc.leader.leader_yolo()
    'YOLO'

We can now manipulate the output of an implicitly added tool:

    >>> xc.runner_mocks.config.get_state.return_value = "1"
    >>> xc.config.get_state(key="wat")
    1

We can clean up our class tree registrations so our tests are
isolated::

    >>> xc.runner_mock_cleanup()

So in one example, we've seen:

 * how to simply manage "tool" subprocess mocking (avoid stacks of mock.patch decorator or sideeffect whackamole)
 * arbitrary alteration of the object structure at initialization time
 * simple extension of namespaces by decorator (to a sideeffecting function)

The current api provides decorators for register child namespaces to
existing namespaces (available to any subclass of
`charmbase.model.namespace`), and a decorator for registering tools
(available to any subclass of
`charmbase.model.namespace.ToolNamespace`).
charmbase.model.context.ExecutionContext` is a tool namespace and may
register both tools and child namespaces.