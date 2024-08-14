from py_secure_shell_automator.user_operations import SSHUserOperations
from . import py_ssh


def test_create_user(py_ssh: SSHUserOperations): ...


def test_delete_user(py_ssh: SSHUserOperations): ...


def test_kill_process(py_ssh: SSHUserOperations): ...
