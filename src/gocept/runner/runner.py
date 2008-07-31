# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
"""Infrastructure for running."""

import os
import time

import ZODB.POSException
import transaction
import zope.app.component.hooks
import zope.app.twisted.main
import zope.app.wsgi
import zope.app.appsetup.product


def main_loop(app, ticks, worker):
    old_site = zope.app.component.hooks.getSite()
    zope.app.component.hooks.setSite(app)
    while True:
        transaction.begin()
        try:
            sleep = worker()
        except (KeyboardInterrupt, SystemExit):
            transaction.abort()
            break
        except Exception, e:
            log.exception(e)
            transaction.abort()
        else:
            try:
                transaction.commit()
            except ZODB.POSException.ConflictError, e:
                log.exception(e)
                transaction.abort()
                # Silently ignore this. The next run will be a retry anyways.

        time.sleep(ticks)

    zope.app.component.hooks.setSite(old_site)


class appmain(object):
    """Decorator to simplify the actual entry point functions for main loops.
    """

    def __init__(self, ticks=1):
        self.ticks = ticks

    def __call__(self, worker_method):
        def configure(appname, configfile):
            app = init(appname, configfile)
            main_loop(app, self.ticks, worker_method)

        # Just to make doctests look nice.
        configure.__name__ = worker_method.__name__
        return configure


def init(appname, configfile):
    """Initialise the Zope environment (without network servers) and return a
    specific root-level object.
    """
    options = zope.app.twisted.main.load_options(['-C', configfile])
    zope.app.appsetup.product.setProductConfigurations(options.product_config)

    db = zope.app.wsgi.config(
        configfile,
        schemafile=os.path.join(
            os.path.dirname(zope.app.twisted.main.__file__), 'schema.xml'))

    root = db.open().root()
    app = root['Application']
    if appname is not None:
        app = application[app]
    return app
