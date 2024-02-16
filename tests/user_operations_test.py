from py_secure_shell_automator.user_operations import SSHUserOperations
from . import ssh


def test_create_user(ssh: SSHUserOperations): ...


def test_delete_user(ssh: SSHUserOperations): ...


def test_kill_process(ssh: SSHUserOperations): ...
