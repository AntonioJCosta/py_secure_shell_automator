"""
Module containing custom exceptions for the process_operations module
"""


class KillProcessError(Exception):
    """
    Raised when there is an error killing a process.
    """

    ...


class GetProcessesStatusError(Exception):
    """
    Raised when there is an error listing processes.
    """

    ...
