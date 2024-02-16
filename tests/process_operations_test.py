from py_secure_shell_automator.processes_operations import SSHProcessOperations
from . import ssh


def test_get_all_running_processes(ssh: SSHProcessOperations):
    processes = ssh.get_all_running_processes()
    assert isinstance(processes, list)


def test_get_single_process_status(ssh: SSHProcessOperations): ...


def test_kill_process(ssh: SSHProcessOperations): ...
