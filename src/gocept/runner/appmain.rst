Creating runners
================

The ``gocept.runner`` package allows it to *easily* create small, long running
scripts which interact with the ZODB. The scripts have the full component
architecture set up when they're run.

Runners are defined with the appmain decorator:

>>> import logging
>>> import gocept.runner
>>> work_count = 0
>>> @gocept.runner.appmain(ticks=0.1)
... def worker():
...     import zope.app.appsetup.product
...     log = logging.getLogger('test')
...     log.info("Working")
...     log.info(sorted(
...         zope.app.appsetup.product.getProductConfiguration('test').items()))
...     global work_count
...     work_count += 1
...     if work_count >= 3:
...         return gocept.runner.Exit


The decorated worker takes two arguments now:

1. The name of an object in the root which will be set as site or None for the
   root.
2. The path to a configuration file (zope.conf)

Create a simple zope.conf:

>>> import os.path
>>> import tempfile
>>> zodb_path = tempfile.mkdtemp()
>>> site_zcml = os.path.join(
...     os.path.dirname(__file__), 'ftesting.zcml')
>>> fd, zope_conf = tempfile.mkstemp()
>>> zope_conf_file = os.fdopen(fd, 'w')
>>> _ = zope_conf_file.write('''\
... site-definition %s
... <zodb>
...   <filestorage>
...     path %s/Data.fs
...   </filestorage>
... </zodb>
... <product-config test>
...     foo bar
...     test-principal zope.mgr
... </product-config>
... <eventlog>
...   <logfile>
...     formatter zope.exceptions.log.Formatter
...     path STDOUT
...   </logfile>
... </eventlog>
... ''' % (site_zcml, zodb_path))
>>> zope_conf_file.close()


So call the worker:

>>> worker(None, zope_conf)
------
... INFO test Working
------
... INFO test [('foo', 'bar'), ('test-principal', 'zope.mgr')]
------
... INFO test Working
------
... INFO test [('foo', 'bar'), ('test-principal', 'zope.mgr')]
------
... INFO test Working
------
... INFO test [('foo', 'bar'), ('test-principal', 'zope.mgr')]



Signals
-------

The worker-procss can be terminated by SIGTERM and SIGHUP in a sane way. Write
a script to a temporary file:

>>> import sys
>>> runner_path = os.path.abspath(
...     os.path.join(os.path.dirname(__file__), '..', '..'))
>>> fd, script_name = tempfile.mkstemp(suffix='.py')
>>> exchange_fd, exchange_file_name = tempfile.mkstemp()
>>> script = os.fdopen(fd, 'w')
>>> _ = script.write("""\
... import sys
... sys.path[0:0] = %s
... sys.path.insert(0, '%s')
... import gocept.runner
...
... f = open('%s', 'w')
...
... @gocept.runner.appmain(ticks=0.1)
... def worker():
...     f.write("Working.\\n")
...     f.flush()
...
... worker(None, '%s')
... """ % (sys.path, runner_path, exchange_file_name, zope_conf))
>>> script.close()


Call the script and wait for it to produce some output:

>>> import signal
>>> import subprocess
>>> import time
>>> exchange = os.fdopen(exchange_fd, 'r+')
>>> proc = subprocess.Popen(
...     [sys.executable, script_name],
...     stdout=subprocess.PIPE,
...     text=True)
>>> while not exchange.read():
...     time.sleep(0.1)
...     _ = exchange.seek(0, 0)
>>> _ = exchange.seek(0, 0)
>>> print(exchange.read())
Working...


Okay, now kill it:

>>> os.kill(proc.pid, signal.SIGTERM)

Wait for the process to really finish and get the output. The runner logs that
it was terminated:

>>> stdout, stderr = proc.communicate()
>>> print(stdout)
------...INFO gocept.runner.runner Received signal 15, terminating...


This also works with SIGHUP:

>>> _ = exchange.truncate(0)
>>> proc = subprocess.Popen(
...     [sys.executable, script_name],
...     stdout=subprocess.PIPE,
...     text=True)
>>> while not exchange.read():
...     time.sleep(0.1)
...     _ = exchange.seek(0, 0)
>>> _ = exchange.seek(0, 0)
>>> print(exchange.read())
Working...

Okay, now kill it:

>>> os.kill(proc.pid, signal.SIGHUP)
>>> stdout, stderr = proc.communicate()
>>> print(stdout)
------...INFO gocept.runner.runner Received signal 1, terminating...


Clean up:
>>> exchange.close()
>>> os.remove(script_name)
>>> os.remove(exchange_file_name)


Setting the principal
---------------------

It is also prossible to create a main loop which runs in an interaction:

>>> def get_principal():
...     return 'zope.mgr'

>>> import zope.security.management
>>> work_count = 0
>>> def interaction_worker():
...     global work_count
...     work_count += 1
...     if work_count >= 3:
...         raise SystemExit(1)
...     log = logging.getLogger('test')
...     interaction = zope.security.management.getInteraction()
...     principal = interaction.participations[0].principal
...     log.info("Working as %s" % principal.id)
>>> worker = gocept.runner.appmain(ticks=0.1, principal=get_principal)(
...     interaction_worker)

Call the worker now:

>>> worker(None, zope_conf)
------
... INFO test Working as zope.mgr
------
... INFO test Working as zope.mgr


After the worker is run there is no interaction:

>>> zope.security.management.queryInteraction() is None
True

It's quite common to read the principal from zope.conf. Therefore there is a
helper which makes this task easier:

>>> work_count = 0
>>> worker = gocept.runner.appmain(
...     ticks=0.1,
...     principal=gocept.runner.from_config('test', 'test-principal'))(
...     interaction_worker)
>>> worker(None, zope_conf)
------
... INFO test Working as zope.mgr
------
... INFO test Working as zope.mgr


Subsites
--------

It is possible to directly work on sites inside the root. The site must already
exist of course, otherwise there will be an error:

>>> worker('a-site', zope_conf)
Traceback (most recent call last):
    ...
KeyError: 'a-site'


Clean up:

>>> import shutil
>>> shutil.rmtree(zodb_path)
>>> os.remove(zope_conf)
