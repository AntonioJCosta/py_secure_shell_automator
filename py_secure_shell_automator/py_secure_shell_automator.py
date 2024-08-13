from .files_operations import SSHFileOperations
from .get_system_info import SSHSystemInfo
from .processes_operations import SSHProcessOperations
from .user_operations import SSHUserOperations

class PySecureShellAutomator(
    SSHFileOperations, SSHProcessOperations, SSHUserOperations, SSHSystemInfo
):
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
            Simple command usage:
            >>> from py_secure_shell_automator import PySecureShellAutomator
            >>> py_ssh = PySecureShellAutomator(host='hostname', username='user_name', password='password')
            >>> cmd_response = py_ssh.run_cmd(cmd='whoami')
            >>> print(cmd_response.ext_code)  # Output: 0
            >>> print(cmd_response.out)  # Output: 'user_name'
            >>> print(cmd_response.is_successful)  # Output: True

            Execute a command as a different user:
            >>> cmd_response = py_ssh.run_cmd(user='another_user', cmd='whoami')
            >>> print(cmd_response.out)  # Output: 'another_user'

            Execute a command as root:
            >>> cmd_response = py_ssh.run_cmd(user='root', cmd='whoami')
            >>> print(cmd_response.out)  # Output: 'root'
        
    Read more in the
    [PySecureShellAutomator documentation](https://github.com/AntonioJCosta/py_secure_shell_automator/).
    """
    