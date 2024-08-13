"""
Module containing methods to manage users
"""

from .exceptions import *
from ..base_ssh import BaseSSH


class SSHUserOperations(BaseSSH):
    """
    Class containing methods to manage users on a remote host.
    """

    def create_user(
        self, username: str, password: str, run_as_root: bool = True
    ) -> None:
        """
        Create a new user on the remote host.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.
            run_as_root (bool): Whether to run the command as root. Default is True.

        Raises:
            UserCreationError: If there is an error creating the user.

        Examples:
            >>> py_ssh.create_user(username='newuser', password='newpassword')
        """
        # Create the user
        create_user_cmd = f"useradd -m {username}"
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=create_user_cmd,
            custom_exception=UserCreationError,
        )

        # Set the user's password
        set_password_cmd = f"echo '{username}:{password}' | sudo chpasswd"
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=set_password_cmd,
            custom_exception=UserCreationError,
        )

    def delete_user(self, username: str, run_as_root: bool = True) -> None:
        """
        Delete a user on the remote host.

        Args:
            username (str): The username of the user to delete.
            run_as_root (bool): Whether to run the command as root. Default is True.

        Raises:
            UserDeletionError: If there is an error deleting the user.

        Examples:
            >>> py_ssh.delete_user(username='olduser')
        """
        # Delete the user
        delete_user_cmd = f"userdel -r {username}"
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=delete_user_cmd,
            custom_exception=UserDeletionError,
        )
