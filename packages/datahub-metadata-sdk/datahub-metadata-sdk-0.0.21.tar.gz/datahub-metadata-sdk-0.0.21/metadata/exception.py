# -*- encoding: utf-8 -*-

"""
Metadata Error & Exception

- [Python3 Exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
"""


class MetadataError(Exception):
    pass


class MetadataValueError(MetadataError, ValueError):
    pass


class MetadataTypeError(MetadataError, TypeError):
    pass


class MetadataAssertionError(MetadataError, AssertionError):
    pass


class MetadataContextError(MetadataError):
    pass


class MetadataPermissionError(MetadataError):
    pass


class MetadataException(Exception):
    pass
