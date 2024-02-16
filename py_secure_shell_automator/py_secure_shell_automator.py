"""
PySecureShellAutomator: A Comprehensive SSH Management Library in Python

PySecureShellAutomator is a robust and versatile Python library that simplifies the process of managing remote Unix hosts via SSH. 
It's built on top of the powerful Paramiko library, but provides a more user-friendly, high-level interface for executing commands 
and transferring files over SSH.

Key Features:
- File Operations: Perform various file operations on the remote host, such as reading, writing, and modifying files.
- Process Operations: Manage processes on the remote host, including starting, stopping, and monitoring processes.
- User Operations: Manage user accounts on the remote host, including creating, modifying, and deleting users.
- System Information Retrieval: Retrieve comprehensive system information from the remote host, such as hardware details, operating system information, and more.

Whether you're a system administrator managing multiple remote servers, a developer working on a distributed system, or a researcher conducting experiments on remote machines, PySecureShellAutomator provides the tools you need to manage your remote systems effectively and efficiently.
"""

from .files_operations import SSHFileOperations
from .get_system_info import SSHSystemInfo
from .processes_operations import SSHProcessOperations
from .user_operations import SSHUserOperations


class PySecureShellAutomator(
    SSHFileOperations, SSHProcessOperations, SSHUserOperations, SSHSystemInfo
):
    """
        PySecureShellAutomator is a robust and versatile Python library that simplifies the process of managing remote Unix hosts via SSH.

        This class provides a high-level interface for executing commands and transferring files over SSH. It includes methods for file operations, process operations, user operations, and system information retrieval.

        Example usage:

            # Use the PySecureShellAutomator instance to perform operation

    ssh = PySecureShellAutomator("hostname", "username", "password")

    processes = ssh.get_all_running_processes()

    for process in processes:
        print(f"User: {process.user}, PID: {process.pid}, CPU: {process.cpu}, MEM: {process.mem}, Command: {process.command}")

        >>> User: root, PID: 1, CPU: 0.1, MEM: 1.4, Command: /sbin/init
        User: daemon, PID: 2, CPU: 0.0, MEM: 0.1, Command: /usr/sbin/atd -f
        User: root, PID: 3, CPU: 0.2, MEM: 0.8, Command: /usr/sbin/cron -f
        User: root, PID: 4, CPU: 0.5, MEM: 2.6, Command: /usr/sbin/rsyslogd -n
        User: syslog, PID: 5, CPU: 0.0, MEM: 0.3, Command: /usr/sbin/rsyslogd -n
        User: root, PID: 10, CPU: 0.3, MEM: 1.4, Command: /sbin/dhclient -1 -v -pf /run/dhclient.eth0.pid -lf /var/lib/dhcp/dhclient.eth0.leases eth0
        User: root, PID: 11, CPU: 0.0, MEM: 0.1, Command: /sbin/agetty --noclear tty1 linux
        User: root, PID: 12, CPU: 0.0, MEM: 0.1, Command: /sbin/agetty --keep-baud 115200 38400 9600 ttyS0 vt220
        User: root, PID: 13, CPU: 0.4, MEM: 2.2, Command: /usr/lib/postfix/sbin/master -w
        User: www-data, PID: 14, CPU: 2.0, MEM: 4.0, Command: /usr/sbin/apache2 -k start
    """
