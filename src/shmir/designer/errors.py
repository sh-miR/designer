"""
.. module:: shmir.designer.error
    :synopsis: This module has all possible exceptions
"""
import logging

error = 'insert only one siRNA sequence or both strands of one' \
        'siRNA at a time; check if both stands are in 5-3 orientation'
len_error = "sequence(s) to long or to short"
patt_error = 'sequence(s) can contain only {actgu} letters'


class BaseException(Exception):
    """
    Base exception class.
    """
    def __init__(self, message=None):
        self.message = message
        logging.error('%s: %s', self.__class__.__name__, self.message)
        super(BaseException, self).__init__(self.message)


class ValidationError(BaseException):
    """Exception error class for incorrect input"""
    pass


class IncorrectDataError(BaseException):
    """Exception error class for incorrect data input"""
    pass


class NoResultError(BaseException):
    """Exception error class for no results"""
    pass
