Changes
=======

3.1 (unreleased)
----------------

- Nothing changed yet.


3.0 (2023-07-20)
----------------

- Drop support for Python 2.7.

- Add support for Python 3.9, 3.10, 3.11.


2.2 (2020-09-14)
----------------

- Get rid of `ZODB3` dependency.


2.1 (2019-12-02)
----------------

- Add support for Python 3.7 and 3.8.

- Migrate to Github.


2.0 (2018-03-14)
----------------

- Backwards incompatible change: No longer depend on ``zope.app.server``,
  and no longer superfluously use its `ZConfig` schema, which superfluously
  requires an `<accesslog>` section that does not make any sense in our context
  anyway. So `<accesslog>` is no longer allowed in the ZConfing config file
  used by this package.


1.0 (2016-01-12)
----------------

- No longer depend on ``zope.app.component``.


0.7.1 (2015-01-28)
------------------

- Fix faulty release 0.7.0.


0.7.0 (2015-01-28)
------------------

- An error message is correctly logged when the worker produces an exception
  which cannot be represented in us-ascii. This used to cause an exception in
  the logging module. The cause of those exceptions where quite hard to track.

- Removed dependency on zope.app.security which was neither declared nor
  necessary.

- Moved project home to <https://bitbucket.org/gocept/gocept.runner/>.


0.6.0 (2011-12-01)
------------------

- Added transaction_per_item decorator.
- Use stdlib's doctest instead of zope.testing.


0.5.3 (2010-04-14)
------------------

- Use log.error/log.warning instead of log.exception. Conflict errors are
  logged as warning now, because they are not really a problem.

0.5.2 (2010-04-14)
------------------

- Convert logged exceptions to str.


0.5.1 (2009-10-13)
------------------

- Declared dependencies correctly.


0.5 (2009-09-21)
++++++++++++++++

- Does no longer use ``zope.app.twisted`` but ``zope.app.server`` instead.


0.4 (2009-09-03)
++++++++++++++++

- The principal set by appmain/once can be computed by a function now.

0.3.2 (2009-05-21)
------------------

- Fixed handling of subsites in appmain.

0.3.1 (2009-05-21)
------------------

- Declared namespace package.

0.3 (2009-04-15)
++++++++++++++++

- When a worker fails the default sleep time (instead of the last one) will be
  used.

0.2 (2009-04-09)
++++++++++++++++

- Added a clean way to exit the runner (by returning gocept.runner.Exit).

0.1 (2009-04-07)
++++++++++++++++

- first public release
