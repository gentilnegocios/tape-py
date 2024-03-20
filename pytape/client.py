# -*- coding: utf-8 -*-
from . import resources


class FailedRequest(Exception):
    def __init__(self, error):
        super(FailedRequest).__init__()
        self.error = error

    def __str__(self):
        return repr(self.error)


# noinspection PyMethodMayBeStatic
class Client(object):
    """
    The Tape API client
    """

    def __init__(self, transport):
        self.transport = transport

    def __getattr__(self, name):
        new_transport = self.transport
        resource = getattr(resources, name)
        return resource(new_transport)

    def __dir__(self):
        """
        Return a list of attribute names.
        """
        return dir(resources)
