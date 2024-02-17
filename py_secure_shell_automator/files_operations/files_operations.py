"""
Module containing files operations for the py_secure_shell_automator module
"""

from .exceptions import *
from ..base_ssh import BaseSSH
from ..models import Directory


class SSHFileOperations(BaseSSH):
    """
    Class to perform files operations on a remote machine
    """

    def copy_file_to_remote(self, local_path: str, remote_path: str) -> None:
        """
        Copies a file from the local machine to the remote host.

        Parameters:
            local_path: Path to the file on the local machine
            remote_path: Path where the file should be copied to on the remote host
        """
        if not self._is_sftp_initialized:
            raise SFTPNotInitializedError("SFTP is not initialized")
        try:
            self._sftp.put(local_path, remote_path)
        except Exception as e:
            raise FileTransferError(f"Error copying file to remote: {e}")

    def copy_file_from_remote(self, remote_path: str, local_path: str) -> None:
        """
        Copies a file from the remote host to the local machine.

        Parameters:
            remote_path: Path to the file on the remote host
            local_path: Path where the file should be copied to on the local machine
        """
        if not self._is_sftp_initialized:
            raise SFTPNotInitializedError("SFTP is not initialized")
        try:
            self._sftp.get(remote_path, local_path)
        except Exception as e:
            raise FileTransferError(f"Error copying file from remote: {e}")

    def get_file_content(self, filepath: str, run_as_root: bool = False) -> str:
        """
        Get the content of a file as a string

        Parameters:
            filepath: Path to the file to read

        Returns:
            Content of the file as a string
        """
        cmd = f"cat {filepath}"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetFileContentError,
        )
        print(cmd_response.ext_code)
        return cmd_response.out

    def remove_file(
        self,
        filepath: str,
        force: bool = False,
        run_as_root: bool = False,
    ) -> None:
        """
        Remove a file

        parameters:
            filepath: the path to the file to remove
            force: if True, remove the file even if it's write-protected
        """
        cmd = f'rm -f "{filepath}"' if force else f'rm "{filepath}"'
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=FileRemovalError,
        )
        return None

    def remove_directory(
        self,
        dirpath: str,
        force: bool = False,
        run_as_root: bool = False,
    ) -> None:
        """
        Remove a directory

        parameters:
            dirpath: the path to the directory to remove
            force: if True, remove the directory even if it's not empty
        """
        cmd = f'rm -rf "{dirpath}"' if force else f'rm -r "{dirpath}"'
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=DirectoryRemovalError,
        )
        return None

    def create_directory(self, dirpath: str, run_as_root: bool = False) -> None:
        """
        Create a directory

        parameters:
            dirpath: the path to the directory to create
        """
        cmd = f'mkdir -p "{dirpath}"'  # Wrap dirpath in quotes
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=DirectoryCreationError,
        )
        return None

    def get_directory_structure(
        self, path: str, run_as_root: bool = False
    ) -> list[Directory]:
        """
        List the content of a directory

        Parameters:
            path: the path to the directory to list
            run_as_root: whether to run the command with root user privileges

        Returns:
            list[Directory]: a list of Directory objects representing each directory and its files

        Raises:
            ListDirectoryContentError: raised if the command fails
        """
        directories_command = f"find {path} -type d"
        directories_response = self.run_cmd(
            user="root" if run_as_root else None,
            cmd=directories_command,
            custom_exception=ListDirectoryContentError,
        )

        directory_structure: list[Directory] = []
        for dir in directories_response.out.splitlines():
            files_command = f"find {dir} -maxdepth 1 -type f"
            files_response = self.run_cmd(
                user="root" if run_as_root else None,
                cmd=files_command,
                custom_exception=ListDirectoryContentError,
            )
            # Get just the file name, not the full path
            files = [file.split("/")[-1] for file in files_response.out.splitlines()]
            directory_structure.append(Directory(dir=dir, files=files))

        return directory_structure

    def change_owner(
        self,
        path: str,
        owner: str,
        recursive: bool = False,
        run_as_root: bool = False,
    ) -> None:
        """
        Change the owner of a file or directory

        Parameters:
            path: the path to the file or directory
            owner: the new owner
            recursive: if True, change the owner recursively
        """

        cmd = f"chown -R {owner} {path}" if recursive else f"chown {owner} {path}"
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=OwnerChangeError,
        )
        return None
