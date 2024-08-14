from py_secure_shell_automator.processes_operations import SSHProcessOperations
from . import py_ssh


def test_get_all_running_processes(py_ssh: SSHProcessOperations):
    processes = py_ssh.get_all_running_processes()
    assert isinstance(processes, list)
    assert processes
    


def test_get_single_process_status(py_ssh: SSHProcessOperations): ...


def test_kill_process(py_ssh: SSHProcessOperations): ...
