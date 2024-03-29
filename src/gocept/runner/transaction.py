# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt
import decorator
import logging
import transaction
import ZODB.POSException


log = logging.getLogger(__name__)


@decorator.decorator
def transaction_per_item(func):
    for action in func():
        try:
            action()
        except Exception as e:
            log.error("Error in item %s: %s", action, e, exc_info=True)
            transaction.abort()
        else:
            try:
                transaction.commit()
            except ZODB.POSException.ConflictError:
                log.warning("Conflict error", exc_info=True)
                transaction.abort()
