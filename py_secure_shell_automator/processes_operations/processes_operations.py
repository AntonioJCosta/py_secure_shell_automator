"""
Module containing processes operations for the py_secure_shell_automator module
"""

from .exceptions import *
from ..models import Process
from ..base_ssh import BaseSSH


class SSHProcessOperations(BaseSSH):
    """
    Class containing process operations for the py_secure_shell_automator module
    """

    def get_single_process_status(
        self, process: str, run_as_root: bool = False
    ) -> list[Process] | None:
        """
        Get the status of all process of a given name on the remote host.

        Parameters:
            process: Name of the process to check
            run_as_root: Whether to run the command as root. Default is False.

        Returns:
            A list of Process objects representing the informed running processes

        Raises:
            GetProcessStatusError: raised if there is an error while getting the process status
        """
        cmd = f"ps aux | grep {process} | grep -v grep"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            raise_exception=False,
            err_message=f"Process {process} not found",
        )

        processes = []
        for line in cmd_response.out.split("\n"):
            fields = line.split()
            if fields:
                processes.append(
                    Process(
                        user=fields[0],
                        pid=int(fields[1]),
                        cpu=float(fields[2]),
                        mem=float(fields[3]),
                        command=" ".join(fields[10:]),
                    )
                )

        return processes or None

    def kill_process(self, process: str, run_as_root: bool = False) -> None:
        """
        Kill a process on the remote host.

        Parameters:
            process: Name of the process to kill
            run_as_root: Whether to run the command as root. Default is False.

        Raises:
            KillProcessError: raised if there is an error while killing the process
        """
        cmd = f"pkill {process}"
        self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=KillProcessError,
        )
        return None

    def get_all_running_processes(self, run_as_root: bool = False) -> list[Process]:
        """
        Get all running processes on the remote host.

        Returns:
            list[Process]: List of Process objects representing the running processes
            run_as_root: Whether to run the command as root. Default is False.

        Raises:
            GetProcessesStatusError: raised if there is an error while getting the process status
        """
        cmd = "ps aux"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetProcessesStatusError,
        )

        processes = []
        for line in cmd_response.out.splitlines()[1:]:  # Skip the header line
            fields = line.split()
            command_start_index = line.index(fields[10])
            command = line[command_start_index:]
            process = Process(
                user=fields[0],
                pid=int(fields[1]),
                cpu=float(fields[2]),
                mem=float(fields[3]),
                command=command,
            )
            processes.append(process)

        return processes
