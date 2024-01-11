"""
Module containing custom exceptions for the process_operations module
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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
