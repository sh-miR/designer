#usr/bin/env python

import logging


class InputException(Exception):
    """Exception error class for incorrect input"""

    def __init__(self, message=None):
        self.message = message
        logging.error('%s: %s', self.__class__.__name__, self.message)
        super(InputException, self).__init__(self.message)