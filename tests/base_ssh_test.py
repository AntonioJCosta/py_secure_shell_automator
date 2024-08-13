import pytest

from py_secure_shell_automator import PySecureShellAutomator
from . import py_ssh

def test_hostname(py_ssh: PySecureShellAutomator):
    hostname = py_ssh.hostname
    assert isinstance(hostname, str)


def test_run_cmd(py_ssh: PySecureShellAutomator):
    cmd_response = py_ssh.run_cmd("echo Hello, World!")
    assert cmd_response.ext_code == 0
    assert cmd_response.out == "Hello, World!"
    assert cmd_response.is_successful is True


def test_run_cmd_with_raise_exception(py_ssh: PySecureShellAutomator):
    with pytest.raises(Exception):
        py_ssh.run_cmd("inexistent command")


def test_run_cmd_without_raise_exception(py_ssh: PySecureShellAutomator):
    py_ssh.run_cmd("inexistent command", raise_exception=False)
