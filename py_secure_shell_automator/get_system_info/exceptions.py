"""
Module containing custom exceptions for the get_system_info module
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class GetSystemInfoError(Exception):
    """
    Raised when there is an error getting the cpu usage.
    """

    ...
