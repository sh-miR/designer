#/usr/bin/env python
"""
.. module:: shmir.designer.error
    :synopsis: This module has all possible exceptions
"""
import logging

ORIENTATION_ERROR = (
    'insert only one siRNA sequence or both strands of one'
    'siRNA at a time; check if both stands are in 5-3 orientation'
)
LENGTH_ERROR = "sequence(s) too long or too short"
PATTERN_ERROR = 'sequence(s) can contain only {actgu} letters'
CUT_WARNING = "cut 'UU' or 'TT'"


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


class IncorrectDataError(BaseException):
    """Exception error class for incorrect data input"""


class NoResultError(BaseException):
    """Exception error class for no results"""
