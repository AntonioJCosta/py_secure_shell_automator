"""
Module containing custom exceptions for the py_secure_shell_automator module
"""


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
