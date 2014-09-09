#usr/bin/env python
import logging

error = 'insert only one siRNA sequence or both strands of one' \
        'siRNA at a time; check if both stands are in 5-3 orientation'
len_error = "to long or to short"
patt_error = 'sequence can contain only {actgu} letters'


class BaseException(Exception):
    def __init__(self, message=None):
        self.message = message
        logging.error('%s: %s', self.__class__.__name__, self.message)
        super(BaseException, self).__init__(self.message)


class InputException(BaseException):
    """Exception error class for incorrect input"""
    pass


class IncorrectDataError(BaseException):
    pass


class NoResultError(BaseException):
    pass
