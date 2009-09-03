# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

from zope.testing import doctest
import os.path
import unittest
import zope.app.testing.functional


runner_layer = zope.app.testing.functional.ZCMLLayer(
    os.path.join(os.path.dirname(__file__), 'ftesting.zcml'),
    __name__, 'RunnerLayer', allow_teardown=True)


def test_suite():
    suite = unittest.TestSuite()
    test = zope.app.testing.functional.FunctionalDocFileSuite(
        'README.txt',
        optionflags=doctest.INTERPRET_FOOTNOTES|doctest.ELLIPSIS)
    test.layer = runner_layer
    suite.addTest(test)

    suite.addTest(doctest.DocFileSuite(
        'appmain.txt',
        'once.txt',
        optionflags=doctest.ELLIPSIS))

    return suite
