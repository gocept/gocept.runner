Runner
======

The ``gocept.runner`` package allows it to *easily* create small, long running
scripts which interact with the ZODB. The scripts have the full component
architecture set up when they're run.

XXX add some "end user" documentation here

Main loop
+++++++++

The main loop loops until it encounters a KeyboardInterrupt or a SystemExit
exception and calls the worker once a second.

Define a worker function which exits when it is called the 3rd time:

>>> work_count = 0
>>> def worker():
...     print "Working"
...     global work_count
...     work_count += 1
...     if work_count >= 3:
...         raise SystemExit(1)


Call the main loop:

>>> import gocept.runner.runner
>>> gocept.runner.runner.main_loop(getRootFolder(), 0.1, worker)
Working
Working
Working
>>> work_count
3


During the loop the site is set:

>>> import zope.app.component.hooks
>>> zope.app.component.hooks.getSite() is None
True
>>> def worker():
...     print zope.app.component.hooks.getSite()
...     raise SystemExit(1)
>>> gocept.runner.runner.main_loop(getRootFolder(), 0.1, worker)
<zope.app.folder.folder.Folder object at 0x1f830f0>



After the loop, no site is set again:

>>> zope.app.component.hooks.getSite() is None
True


When the worker passes without error a transaction is commited:

>>> work_count = 0
>>> def worker():
...     print "Working"
...     global work_count
...     work_count += 1
...     if work_count >= 2:
...         raise SystemExit(1)
...     site = zope.app.component.hooks.getSite()
...     site.worker_done = 1
>>> gocept.runner.runner.main_loop(getRootFolder(), 0.1, worker)
Working
Working

We have set the attribute ``worker_done`` now:

>>> getRootFolder().worker_done
1


When the worker produces an error, the transaction is aborted:

>>> def worker():
...     print "Working"
...     site = zope.app.component.hooks.getSite()
...     site.worker_done = 2
...     raise SystemExit(1)
>>> gocept.runner.runner.main_loop(getRootFolder(), 0.1, worker)
Working


We still have the attribute ``worker_done`` set to 1:b

>>> getRootFolder().worker_done
1
