import pytest
from py_secure_shell_automator.files_operations import SSHFileOperations
from . import *


@pytest.fixture
def ssh_file_ops() -> SSHFileOperations:
    return SSHFileOperations(
        host=PYSECURE_SHELL_AUTOMATOR_HOST,
        username=PYSECURE_SHELL_AUTOMATOR_USERNAME,
        password=PYSECURE_SHELL_AUTOMATOR_PASSWORD,
        port=PYSECURE_SHELL_AUTOMATOR_PORT,
        sftp=True,
    )


def test_sftp_not_initialized(py_ssh: SSHFileOperations):
    """
    The function `test_sftp_not_initialized` takes an instance of `SSHFileOperations`
    and tries to execute a method that requires an SFTP connection to be established.

    Parameters:
    -----------
        ssh_file_ops: An object of the SSHFileOperations class, which provides
        methods for performing file operations on a remote server using SSH
    """

    with pytest.raises(Exception):
        py_ssh.copy_file_to_remote("local_path", "remote_path")


def test_copy_file_to_remote(ssh_file_ops: SSHFileOperations):
    """
    The function `test_copy_file_to_remote` takes an instance of `SSHFileOperations`
    and performs some operations related to copying files to a remote server.

    :param ssh_file_ops: An object of the SSHFileOperations class, which provides
    methods for performing file operations on a remote server using SSH
    :type ssh_file_ops: SSHFileOperations
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(current_dir, "data", "file_test1.txt")

    remote_path = "/tmp/file_test1.txt"
    ssh_file_ops.copy_file_to_remote(local_path, remote_path)


def test_copy_file_from_remote(ssh_file_ops: SSHFileOperations):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(current_dir, "data", "file_test1.txt")

    remote_path = "/tmp/file_test1.txt"
    ssh_file_ops.copy_file_from_remote(remote_path, local_path)


def test_get_file_content(ssh_file_ops: SSHFileOperations):

    filepath = "/tmp/file_test1.txt"
    content = ssh_file_ops.get_file_content(filepath)
    assert isinstance(content, str)
