# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt
"""Infrastructure for running."""

import logging
import os
import time

import ZODB.POSException
import transaction
import zope.app.appsetup.product
import zope.app.security.interfaces
import zope.app.component.hooks
import zope.app.twisted.main
import zope.app.wsgi
import zope.security.management
import zope.security.testing
import zope.publisher.base


log = logging.getLogger(__name__)


class RunnerRequest(zope.publisher.base.BaseRequest):
    """A custom publisher request for the runner."""

    def __init__(self, *args):
        super(RunnerRequest, self).__init__(None, {}, positional=args)


class MainLoop(object):

    def __init__(self, app, ticks, worker, principal=None):
        self.app = app
        self.ticks = ticks
        self.worker = worker
        if principal is None:
            self.interaction = False
        else:
            self.interaction = True
            self.principal_id = principal


    def __call__(self):
        old_site = zope.app.component.hooks.getSite()
        zope.app.component.hooks.setSite(self.app)

        ticks = None

        while True:
            self.begin()
            try:
                ticks = self.worker()
            except (KeyboardInterrupt, SystemExit):
                self.abort()
                break
            except Exception, e:
                log.exception(e)
                self.abort()
            else:
                try:
                    self.commit()
                except ZODB.POSException.ConflictError, e:
                    log.exception(e)
                    self.abort()
                    # Silently ignore this. The next run will be a retry anyways.

            if ticks is None:
                ticks = self.ticks
            log.debug("Sleeping %s seconds" % ticks)
            time.sleep(ticks)

        zope.app.component.hooks.setSite(old_site)

    def begin(self):
        transaction.begin()
        if self.interaction:
            request = RunnerRequest()
            request.setPrincipal(self.principal)
            zope.security.management.newInteraction(request)

    def abort(self):
        transaction.abort()
        if self.interaction:
            zope.security.management.endInteraction()

    def commit(self):
        transaction.commit()
        if self.interaction:
            zope.security.management.endInteraction()

    @property
    def principal(self):
        auth = zope.component.getUtility(
            zope.app.security.interfaces.IAuthentication)
        return auth.getPrincipal(self.principal_id)


class appmain(object):
    """Decorator to simplify the actual entry point functions for main loops.
    """

    def __init__(self, ticks=1, principal=None):
        self.ticks = ticks
        self.principal = principal

    def __call__(self, worker_method):
        def configure(appname, configfile):
            db, app = init(appname, configfile)
            MainLoop(app, self.ticks, worker_method,
                      principal=self.principal)()
            db.close()
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
    return db, app
