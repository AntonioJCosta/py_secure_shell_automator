"""
Module containing custom exceptions for the files_operations module
"""

from .exceptions import *


class FileRemovalError(Exception):
    """
    Raised when there is an error removing a file.
    """

    ...


class SFTPNotInitializedError(Exception):
    """
    Raised when an attempt is made to use SFTP before it is initialized.
    """

    ...


class FileTransferError(Exception):
    """
    Raised when there is an error transferring a file.
    """

    ...


class GetFileContentError(Exception):
    """
    Raised when there is an error getting the content of a file.
    """

    ...


class DirectoryRemovalError(Exception):
    """
    Raised when there is an error removing a directory.
    """

    ...


class DirectoryCreationError(Exception):
    """
    Raised when there is an error creating a directory.
    """

    ...


class ListDirectoryContentError(Exception):
    """
    Raised when there is an error listing files.
    """

    ...


class OwnerChangeError(Exception):
    """
    Exception raised when the change owner operation fails
    """

    ...
