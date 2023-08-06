"""
Collection of custom exception wrappers
"""


class ServerError(Exception):
    pass


class RequestError(Exception):
    pass


class UserNotFoundError(Exception):
    pass
