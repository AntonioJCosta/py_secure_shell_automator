from py_secure_shell_automator.get_system_info.get_system_info import SSHSystemInfo
from . import ssh


def test_get_cpu_usage(ssh: SSHSystemInfo):
    cpu_usage = ssh.get_cpu_usage()
    assert isinstance(cpu_usage, str)


def test_get_memory_usage(ssh: SSHSystemInfo):
    memory_usage = ssh.get_memory_usage()
    assert isinstance(memory_usage, str)


def test_get_disk_usage(ssh: SSHSystemInfo):
    disk_usage = ssh.get_disk_usage()
    assert isinstance(disk_usage, str)


def test_get_kernel_version(ssh: SSHSystemInfo):
    kernel_version = ssh.get_kernel_version()
    assert isinstance(kernel_version, str)


def test_get_os_version(ssh: SSHSystemInfo):
    os_version = ssh.get_os_version()
    assert isinstance(os_version, str)
