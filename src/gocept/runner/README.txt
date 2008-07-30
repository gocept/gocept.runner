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


