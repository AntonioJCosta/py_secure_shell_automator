"""
Module containing methods to get system information
"""

from .exceptions import *
from ..base_ssh import BaseSSH


class SSHSystemInfo(BaseSSH):
    """
    Class containing methods to get system information
    """

    def get_cpu_usage(self, run_as_root: bool = False) -> str:
        """
        Get the CPU usage of the remote host.

        Parameters:
            run_as_root: Whether to run the command as root. Default is False.

        Returns:
            CPU usage as a string
        """
        cmd = "top -b -n1 | grep 'Cpu(s)' | awk '{printf \"%.2f%%\", $2 + $4}'"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetSystemInfoError,
        )
        return cmd_response.out

    def get_memory_usage(self, run_as_root: bool = False) -> str:
        """
        Get the memory usage of the remote host.

        Parameters:
            run_as_root: Whether to run the command as root. Default is False.

        Returns:
            Memory usage as a string
        """
        cmd = "free -m | awk 'NR==2{printf \"%s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetSystemInfoError,
        )
        return cmd_response.out

    def get_disk_usage(self, run_as_root: bool = False) -> str:
        """
        Get the disk usage of the remote host.

        Parameters:
            run_as_root: Whether to run the command as root. Default is False.

        Returns:
            Disk usage as a string
        """
        cmd = 'df -h | awk \'$NF=="/"{printf "%d/%dGB (%s)", $3,$2,$5}\''
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetSystemInfoError,
        )
        return cmd_response.out

    def get_kernel_version(self, run_as_root: bool = False) -> str:
        """
        Get the kernel version of the remote host.

        Parameters:
            run_as_root: Whether to run the command as root. Default is False.

        Returns:
            Kernel version as a string
        """
        cmd = "uname -r"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetSystemInfoError,
        )
        return cmd_response.out

    def get_os_version(self, run_as_root: bool = False) -> str:
        """
        Get the operating system version of the remote host.

        Parameters:
            run_as_root: Whether to run the command as root. Default is False.

        Returns:
            Operating system version as a string
        """
        cmd = "cat /etc/os-release | grep PRETTY_NAME | cut -d '=' -f 2"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetSystemInfoError,
        )
        return cmd_response.out
