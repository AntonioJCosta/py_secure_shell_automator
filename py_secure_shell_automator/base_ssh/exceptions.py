"""
Module containing custom exceptions for the py_secure_shell_automator module
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CmdError(Exception):
    """
    Standard Exception when a command fails
    """

    ...


class AuthenticationError(Exception):
    """
    Raised when there is an error with authentication.
    """

    ...
