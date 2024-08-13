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

        Args:
            run_as_root (bool): Whether to run the command as root. Default is False.

        Returns:
            str: CPU usage.

        Raises:
            GetSystemInfoError: If there is an error retrieving the CPU usage.
            
        Example:
            >>> cpu_usage = py_ssh.get_cpu_usage()
            >>> print(cpu_usage)
            '10.0%'
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

        Args:
            run_as_root (bool): Whether to run the command as root. Default is False.

        Returns:
            str: Memory usage.

        Raises:
            GetSystemInfoError: If there is an error retrieving the memory usage.
            
        Example:
            >>> memory_usage = py_ssh.get_memory_usage()
            >>> print(memory_usage)
            '10/20MB (50%)'
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

        Args:
            run_as_root (bool): Whether to run the command as root. Default is False.

        Returns:
            str: Disk usage.

        Raises:
            GetSystemInfoError: If there is an error retrieving the disk usage.
            
        Example:
            >>> disk_usage = py_ssh.get_disk_usage()
            >>> print(disk_usage)
            '10/20GB (50%)'
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

        Args:
            run_as_root (bool): Whether to run the command as root. Default is False.

        Returns:
            str: Kernel version.

        Raises:
            GetSystemInfoError: If there is an error retrieving the kernel version.
            
        Example:
            >>> kernel_version = py_ssh.get_kernel_version()
            >>> print(kernel_version)
            '5.4.0-42-generic'
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

        Args:
            run_as_root (bool): Whether to run the command as root. Default is False.

        Returns:
            str: Operating system version.

        Raises:
            GetSystemInfoError: If there is an error retrieving the operating system version.
            
        Example:
            >>> os_version = py_ssh.get_os_version()
            >>> print(os_version)
            'Arch Linux'
        """
        cmd = "cat /etc/os-release | grep PRETTY_NAME | cut -d '=' -f 2"
        cmd_response = self.run_cmd(
            user=self._get_user(run_as_root),
            cmd=cmd,
            custom_exception=GetSystemInfoError,
        )
        return cmd_response.out