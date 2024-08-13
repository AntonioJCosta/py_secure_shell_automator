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
        Copies a file from the local machine to the remote host. `SFTP` must be initialized.
    
        The `local_path` and `remote_path` should be absolute paths, including the filename.
    
        If the file already exists at the `remote_path`, it will be overwritten.
    
        Args:
            local_path (str): Absolute path to the file on the local machine.
            remote_path (str): Absolute path where the file should be copied to on the remote host.
    
        Raises:
            SFTPNotInitializedError: If SFTP is not initialized.
            FileTransferError: If there is an error copying the file to the remote host.
    
        Examples:
            >>> py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
            >>> py_ssh.copy_file_to_remote('/absolute/path/to/local/file.txt', '/absolute/path/to/remote/file.txt')
        """
        if not self._is_sftp_initialized:
            raise SFTPNotInitializedError("SFTP is not initialized")
        try:
            self._sftp.put(local_path, remote_path)
        except Exception as e:
            raise FileTransferError(f"Error copying file to remote: {e}")
    
    def copy_file_from_remote(self, remote_path: str, local_path: str) -> None:
        """
        Copies a file from the remote host to the local machine. SFTP must be initialized.
    
        The `remote_path` and `local_path` should be absolute paths, including the filename.
    
        If the file already exists at the `local_path`, it will be overwritten.
    
        Args:
            remote_path (str): Absolute path to the file on the remote host.
            local_path (str): Absolute path where the file should be copied to on the local machine.
    
        Raises:
            SFTPNotInitializedError: If SFTP is not initialized.
            FileTransferError: If there is an error copying the file from the remote host.
    
        Examples:
            >>> py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
            >>> py_ssh.copy_file_from_remote('/absolute/path/to/remote/file.txt', '/absolute/path/to/local/file.txt')
        """
        if not self._is_sftp_initialized:
            raise SFTPNotInitializedError("SFTP is not initialized")
        try:
            self._sftp.get(remote_path, local_path)
        except Exception as e:
            raise FileTransferError(f"Error copying file from remote: {e}")

    def get_file_content(self, filepath: str, run_as_root: bool = False) -> str:
        """
        Gets the content of a file as a string.

        Args:
            filepath (str): Path to the file to read.
            run_as_root (bool, optional): Whether to run the command as root. Defaults to False.

        Returns:
            str: Content of the file as a string.

        Raises:
            GetFileContentError: If there is an error getting the file content.

        Examples:
            >>> content = py_ssh.get_file_content('/path/to/file.txt')
            >>> print(content)
            'File content'
        """
        cmd = f"cat {filepath}"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetFileContentError,
        )
        return cmd_response.out

    def remove_file(
        self,
        filepath: str,
        force: bool = False,
        run_as_root: bool = False,
    ) -> None:
        """
        Remove a file.

        Args:
            filepath (str): The path to the file to remove.
            force (bool, optional): If True, remove the file even if it's write-protected. Defaults to False.
            run_as_root (bool, optional): Whether to run the command as root. Defaults to False.

        Raises:
            FileRemovalError: If there is an error removing the file.

        Examples:
            Remove a file normally
            >>> py_ssh.remove_file('/path/to/file.txt')

            Force remove a write-protected file
            >>> py_ssh.remove_file('/path/to/protected_file.txt', force=True)
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
        Remove a directory.

        This method removes a directory at the specified path. If the directory is not empty,
        the `force` parameter can be used to remove it and all its contents.

        Args:
            dirpath (str): The path to the directory to remove.
            force (bool, optional): If True, remove the directory even if it's not empty. Defaults to False.
            run_as_root (bool, optional): Whether to run the command as root. Defaults to False.

        Raises:
            DirectoryRemovalError: If there is an error removing the directory.

        Examples:
            Remove an empty directory
            >>> py_ssh.remove_directory('/path/to/empty_directory')

            Force remove a non-empty directory
            >>> py_ssh.remove_directory('/path/to/non_empty_directory', force=True)

            Remove a directory as root
            >>> py_ssh.remove_directory('/path/to/directory', run_as_root=True)

            Force remove a non-empty directory as root
            >>> py_ssh.remove_directory('/path/to/non_empty_directory', force=True, run_as_root=True)
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
        Create a directory. If the directory already exists, the command will not fail.

        This method will create the directory and any parent directories if they do not exist.

        Args:
            dirpath (str): The path to the directory to create.
            run_as_root (bool, optional): Whether to run the command as root. Defaults to False.

        Raises:
            DirectoryCreationError: If there is an error creating the directory.

        Examples:
            Create a directory normally
            >>> py_ssh.create_directory('/path/to/new_directory')

            # Create a directory as root
            >>> py_ssh.create_directory('/path/to/new_directory', run_as_root=True)
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
        List the content of a directory on the remote server.

        This method returns a list of Directory objects, each representing a directory and its files.

        Args:
            path (str): The path to the directory to list. This should be an absolute path.
            run_as_root (bool, optional): Whether to run the command with root user privileges. Defaults to False.

        Returns:
            list[Directory]: A list of Directory objects representing each directory and its files.

        Raises:
            ListDirectoryContentError: If the command fails to list the directory content.

        Examples:
            List directory content
            >>> dir_structure = py_ssh.get_directory_structure('/path/to/directory')
            >>> for directory in dir_structure:
            >>>     print(f"Directory: {directory.dir}")
            >>>     print("Files:")
            >>>     for file in directory.files:
            >>>         print(f"{file}")

        Notes:
            - Ensure that the user has the necessary permissions to list the directory content at the specified path.
        """
        directory_structure: list[Directory] = []
        directories_command = f"LC_ALL=C.UTF-8 find {path} -type d"
        directories_response = self.run_cmd(
            user="root" if run_as_root else None,
            cmd=directories_command,
            raise_exception=True,
            custom_exception=ListDirectoryContentError,
        )

        for dir in directories_response.out.splitlines():
            # Use find to list files and then grep to simulate -maxdepth 1 behavior
            files_command = (
                f"LC_ALL=C.UTF-8 find '{dir}' -type f | grep -E \"^{dir}/[^/]+$\""
            )
            files_response = self.run_cmd(
                user="root" if run_as_root else None,
                cmd=files_command,
                raise_exception=False,
            )

            dirs_response_out = files_response.out
            if dirs_response_out == "":
                directory_structure.append(Directory(dir=dir, files=[]))
                continue

            if files_response.ext_code != 0:
                raise ListDirectoryContentError(
                    f"Error listing directory content: {dirs_response_out}"
                )

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
        Change the owner of a file or directory.

        If the `recursive` parameter is set to True, the owner will be changed recursively.

        Args:
            path (str): The path to the file or directory.
            owner (str): The new owner.
            recursive (bool, optional): If True, change the owner recursively. Defaults to False.
            run_as_root (bool, optional): Whether to run the command as root. Defaults to False.

        Raises:
            OwnerChangeError: If there is an error changing the owner.

        Examples:
            Change the owner of a file:
            >>> py_ssh.change_owner('/path/to/file', 'new_owner')

            Change the owner of a directory:
            >>> py_ssh.change_owner('/path/to/directory', 'new_owner')

            Change the owner of a directory and its contents recursively:
            >>> py_ssh.change_owner('/path/to/directory', 'new_owner', recursive=True)
        """
        cmd = f"chown -R {owner} {path}" if recursive else f"chown {owner} {path}"
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=OwnerChangeError,
        )
        return None
