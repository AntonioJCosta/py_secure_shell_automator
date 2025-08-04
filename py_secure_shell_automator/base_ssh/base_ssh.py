"""
Provides the BaseSSH class, which serves as the foundation for establishing SSH connections to remote hosts, using Paramiko library.
"""

import shlex
from dataclasses import dataclass
from paramiko import SSHClient, AutoAddPolicy, RejectPolicy, RSAKey
from typing import Type
from .exceptions import *
from ..models import CmdResponse


@dataclass
class BaseSSH:
    """
    Connects to a remote host using the SSH protocol, and provides methods to execute commands and transfer files.

    Attributes:
        host (str): Host to connect to the remote host.
        username (str): Username to connect to the remote host.
        password (str, optional): Password to connect to the remote host. Defaults to None.
        port (int, optional): Port to connect to the remote host. Defaults to 22.
        pkey (str, optional): Private key to connect to the remote host. Defaults to None.
        timeout (int, optional): Timeout to connect to the remote host. Defaults to 10.
        auth_timeout (int, optional): Authentication timeout to connect to the remote host. Defaults to 10.
        auto_add_policy (bool, optional): Whether to add the host to the known hosts. Defaults to True.
        sftp (bool, optional): Whether to use the SFTP protocol to connect to the remote host. Defaults to False.

    Example:
        ```python
        from py_secure_shell_automator import PySecureShellAutomator

        py_ssh = PySecureShellAutomator(host='hostname', username='admin', password='admin_pass')
        cmd_response = py_ssh.run_cmd(cmd='whoami')
        print(cmd_response.out)  # Output: 'admin'
        ```
    """

    host: str
    username: str
    password: str | None = None
    port: int = 22
    pkey: str | None = None
    timeout: int = 10
    auth_timeout: int = 10
    auto_add_policy: bool = True
    sftp: bool = False

    def __post_init__(self) -> None:
        """
        Create an SSHClient object and set the policy to add the host to the known hosts.
        """
        self._ssh = SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(
            AutoAddPolicy() if self.auto_add_policy else RejectPolicy()
        )
        self._connects()
        if self.sftp:
            self._sftp = self._ssh.open_sftp()
        self._is_sftp_initialized = hasattr(self, "sftp")

    @property
    def hostname(self) -> str:
        """
        Returns the hostname of the remote host.

        Returns:
            str: The hostname of the remote host.
        """
        return self.run_cmd("hostname -s").out

    def run_cmd(
        self,
        cmd: str,
        user: str | None = None,
        raise_exception: bool = True,
        custom_exception: Type[Exception] = CmdError,
        err_message: str | None = None,
        cmd_timeout: float | None = 10,
    ) -> CmdResponse:
        """
        Execute a command on the remote host. If the exit code is not 0, raise an exception.

        Args:
            cmd (str): Command to execute on the remote host.
            user (str, optional): User to execute the command. If None, the user is the same as the one used to connect. Defaults to None.
            raise_exception (bool, optional): If True, raise an exception if the exit code is not 0. Defaults to True.
            custom_exception (Type[Exception], optional): Custom exception to raise if the exit code is not 0 and raise_exception is True. Defaults to CmdError.
            err_message (str, optional): Error message to raise if the exit code is not 0 and raise_exception is True. If None, the output of the command is used. Defaults to None.
            cmd_timeout (float, optional): Timeout to execute the command. Defaults to 10 seconds.

        Returns:
            CmdResponse: Object with the output and exit code of the command.

        Raises:
            custom_exception: Raised if the exit code is not 0 and raise_exception is True.

        Examples:

            Simple command usage:
            >>> cmd_response = py_ssh.run_cmd(cmd='whoami')
            >>> print(cmd_response.ext_code)  # Output: 0
            >>> print(cmd_response.out)  # Output: 'username'
            >>> print(cmd_response.is_successful)  # Output: True

            Execute a command as a different user:
            >>> cmd_response = py_ssh.run_cmd(user='another_user', cmd='whoami')
            >>> print(cmd_response.out)  # Output: 'another_user'

            Execute a command as root:
            >>> cmd_response = py_ssh.run_cmd(user='root', cmd='whoami')
            >>> print(cmd_response.out)  # Output: 'root'

            Dealing with errors:

            1. Using try-except block:
            
            >>> from py_secure_shell_automator.exceptions import CmdError
            >>> try:
                    cmd_response = py_ssh.run_cmd(cmd='wrong_command')
                except CmdError as e:
                    print(e)  # Output: 'bash: wrong_command: command not found'
                    # Continue with the error handling

            2. Using raise_exception=False:
            >>> cmd_response = py_ssh.run_cmd(cmd='wrong_command', raise_exception=False)
            >>> if not cmd_response.is_success:
                    print(cmd_response.out)  # Output: 'bash: wrong_command: command not found'
                    # Continue with the error handling

            3. Dealing with different exit codes:
            >>> cmd_response = py_ssh.run_cmd(cmd='sh /path/to/script.sh', raise_exception=False)
            >>> match cmd_response.ext_code:
                    case 0:
                        print("The script was executed successfully")
                    case 126:
                        print("The script was not executable")
                    case 127:
                        print("The script was not found")
                    case _:
                        print(f"An unknown error occurred with exit code {cmd_response.exit_code}")

            4. Defining a custom exception:
            >>> class CustomError(Exception):
                    pass
            >>> try:
                    cmd_response = py_ssh.run_cmd(cmd='wrong_command', custom_exception=CustomError)
                except Exception as e:
                    # Print the custom error type
                    print(type(e))  # Output: <class '__main__.CustomError'>

            5. Using a custom error message:
            >>> try:
                    cmd_response = py_ssh.run_cmd(cmd='command_with_no_output', err_message='The command failed')
                except CmdError as e:
                    print(e)  # Output: 'The command failed'
        """
        if user:
            user = shlex.quote(user)  # Shell-escape the user
            cmd = (
                f"sudo {cmd}"
                if user == "root"
                else f"""sudo /usr/bin/su - {user} -c "{cmd}" """
            )

        _, stdout, stderr = self._ssh.exec_command(
            cmd, get_pty=True, timeout=cmd_timeout
        )
        ext_code = stderr.channel.recv_exit_status()
        out = stdout.read().decode("utf-8").rstrip()

        # Sometimes cmd_err is empty, so it's used out instead
        cmd_err = stderr.read().decode("utf-8").rstrip() or out

        if ext_code == 0:
            return CmdResponse(ext_code, out)

        if raise_exception:
            raise custom_exception(err_message or cmd_err)

        return CmdResponse(ext_code, cmd_err)

    def _connects(self) -> None:
        """
        Establish an SSH connection to the remote host using the SSH client object.

        This method initializes the SSH connection with the provided host, username,
        and other authentication details. It does not take any parameters and does
        not return any value.

        Raises:
            AuthenticationException: If authentication fails.
            SSHException: If there is any error connecting or establishing an SSH session.
            socket.error: If there is any socket error.
        """

        try:
            if not self.password and not self.pkey:
                raise AuthenticationError(
                    "Either password or private key must be provided"
                )

            # Load the private key if provided, else use password
            if self.pkey:
                private_key = RSAKey(filename=self.pkey)
                self._ssh.connect(
                    hostname=self.host,
                    username=self.username,
                    pkey=private_key,
                    timeout=self.timeout,
                    auth_timeout=self.auth_timeout,
                )
                return None

            self._ssh.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                auth_timeout=self.auth_timeout,
            )
            return None

        except Exception as e:
            raise ConnectionError(f"Error connecting to {self.host}: {e}")

    def _get_user(self, run_as_root: bool) -> str | None:
        """
        Helper method to get the user based on the run_as_root parameter.

        Args:
            run_as_root (bool): Whether to run the command as root.

        Returns:
            str | None: The user to run the command as. Returns "root" if run_as_root is True, otherwise None.
        """
        return "root" if run_as_root else None
