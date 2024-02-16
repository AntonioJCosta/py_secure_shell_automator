import pytest

from py_secure_shell_automator import PySecureShellAutomator
from . import ssh


def test_hostname(ssh: PySecureShellAutomator):
    hostname = ssh.hostname
    assert isinstance(hostname, str)


def test_run_cmd(ssh: PySecureShellAutomator):
    response = ssh.run_cmd("echo Hello, World!")
    assert response.ext_code == 0
    assert response.out == "Hello, World!"
    assert response.is_successful is True


def test_run_cmd_with_raise_exception(ssh: PySecureShellAutomator):
    with pytest.raises(Exception):
        ssh.run_cmd("inexistent command")


def test_run_cmd_without_raise_exception(ssh: PySecureShellAutomator):
    ssh.run_cmd("inexistent command", raise_exception=False)
