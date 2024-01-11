"""
Module containing custom exceptions for the user_operations module
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
