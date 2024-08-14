from py_secure_shell_automator.get_system_info.get_system_info import SSHSystemInfo
from . import py_ssh


def test_get_cpu_usage(py_ssh: SSHSystemInfo):
    cpu_usage = py_ssh.get_cpu_usage()
    assert isinstance(cpu_usage, str)


def test_get_memory_usage(py_ssh: SSHSystemInfo):
    memory_usage = py_ssh.get_memory_usage()
    assert isinstance(memory_usage, str)


def test_get_disk_usage(py_ssh: SSHSystemInfo):
    disk_usage = py_ssh.get_disk_usage()
    assert isinstance(disk_usage, str)


def test_get_kernel_version(py_ssh: SSHSystemInfo):
    kernel_version = py_ssh.get_kernel_version()
    assert isinstance(kernel_version, str)


def test_get_os_version(py_ssh: SSHSystemInfo):
    os_version = py_ssh.get_os_version()
    assert isinstance(os_version, str)
