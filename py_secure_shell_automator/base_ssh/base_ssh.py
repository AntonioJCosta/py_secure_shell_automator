"""
Connects to a linux remote host by ssh connection and
can executes commands on it and returns the output of the command,
using the paramiko library.
"""

import shlex

from dataclasses import dataclass
from typing import Type

from paramiko import AutoAddPolicy, RSAKey, RejectPolicy, SSHClient
from .exceptions import *
from ..models import CmdResponse


@dataclass
class BaseSSH:
    """
    Connects to a linux remote host by ssh protocol, using the
    paramiko library.

    Attributes:
    ----------
        host: Host to connect to the remote host
        username: Username to connect to the remote host
        password: Password to connect to the remote host
        port: Port to connect to the remote host. Default is 22
        pkey: Private key to connect to the remote host
        timeout: Timeout to connect to the remote host. Default is 10
        auth_timeout: Authentication timeout to connect to the remote host. Default is 10
        auto_add_policy: Whether to add the host to the known hosts
        sftp: Whether to use sftp protocol to connect to the remote host
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
        Create a SSHClient object and set the policy to add the host to the known hosts
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
        self._hostname = self.run_cmd("hostname -s", raise_exception=False).out

    @property
    def hostname(self) -> str:
        """
        Returns the hostname of the remote host
        """
        return self._hostname

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
        Execute a command on the remote host. If exit code is not 0, raise an
        exception.

        Parameters:

            cmd: Command to execute on the remote host
            user: User to execute the command. If None, the user is the same as the one used to connect
            raise_exception: If True, raise an exception if the exit code is not 0
            custom_exception: Custom exception to raise if the exit code is not 0 and raise_exception is True
            err_message: Error message to raise if the exit code is not 0 and raise_exception is True. If None, the output of the command is used
            cmd_timeout: Timeout to execute the command. Default is 10 seconds
        Returns:
            CmdResponse: Object with the output and exit code of the command

        Raises:
            custom_exception: raised if the exit code is not 0 and
            raise_exception is True
        """

        cmd = cmd.replace("\n", "").replace("\r", "")  # Remove new lines
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
        Connect to a remote host by ssh protocol, using the ssh client object
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
        Helper method to get the user based on the run_as_root parameter

        Parameters:
            run_as_root: whether to run the command as root

        Returns:
            The user to run the command as
        """
        return "root" if run_as_root else None
