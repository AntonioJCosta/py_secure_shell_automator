"""
Module containing custom exceptions for the user_operations module
"""


class UserCreationError(Exception):
    """
    Raised when there is an error creating a user.
    """

    ...


class UserDeletionError(Exception):
    """
    Raised when there is an error deleting a user.
    """

    ...
