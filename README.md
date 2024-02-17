[![Downloads](https://pepy.tech/badge/py_secure_shell_automator)](https://pepy.tech/project/py_secure_shell_automator)
[![PyPI](https://img.shields.io/pypi/v/py_secure_shell_automator.svg)](https://pypi.python.org/pypi/py_secure_shell_automator)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/py_secure_shell_automator.svg)](https://pypi.python.org/pypi/py_secure_shell_automator/)
[![Build Status](https://travis-ci.org/AntonioJCosta/py_secure_shell_automator.svg?branch=main)](https://travis-ci.org/AntonioJCosta/py_secure_shell_automator)

# PySecureShellAutomator: A Comprehensive SSH Management Library in Python



PySecureShellAutomator is a robust and versatile Python library that simplifies the process of managing remote Unix hosts via SSH. It's built on top of the powerful Paramiko library, but provides a more user-friendly, high-level interface for executing commands and transferring files over SSH.

This library is designed with flexibility in mind, catering to a wide range of use cases. Whether you're automating server tasks, deploying applications, managing cloud infrastructure, or developing software that requires remote execution, PySecureShellAutomator is equipped to handle your needs.

Key features of PySecureShellAutomator include:

- **Easy Connection Management**: PySecureShellAutomator simplifies the process of establishing SSH connections, supporting both password-based and key-based authentication methods. It also provides options for setting connection and authentication timeouts, and automatically adding the host to the known hosts file.

- **Command Execution**: PySecureShellAutomator allows you to execute any command on the remote host and retrieve the output and exit code. It provides options for specifying the user that will execute the command, setting a timeout for the command execution, and handling errors.

- **File Operations**: With PySecureShellAutomator, you can easily transfer files to and from the remote host using the SFTP protocol. It provides methods for copying files and handling file transfer errors.

- **Exception Handling**: PySecureShellAutomator provides custom exceptions for handling specific types of errors, such as command execution errors and file transfer errors. This allows you to easily catch and handle errors in your code.

Whether you're developing a deployment script, automating system administration tasks, or building a web application that interacts with remote servers, PySecureShellAutomator provides the tools you need to manage remote systems with ease.

**We are always open to new pull requests!**

## Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)

## Key Features

- [PySecureShellAutomator: A Comprehensive SSH Management Library in Python](#pysecureshellautomator-a-comprehensive-ssh-management-library-in-python)
  - [Contents](#contents)
  - [Key Features](#key-features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Establishing a Connection](#establishing-a-connection)
    - [Password-based Authentication](#password-based-authentication)
    - [Key-based Authentication](#key-based-authentication)
    - [File Operations](#file-operations)
      - [Copy a File to the Remote Host](#copy-a-file-to-the-remote-host)
      - [Copy a File from the Remote Host](#copy-a-file-from-the-remote-host)
      - [Get Content of a File](#get-content-of-a-file)
      - [Create a Directory](#create-a-directory)
      - [Get Scructure of a Directory](#get-scructure-of-a-directory)
      - [Remove a File](#remove-a-file)
      - [Remove Directory](#remove-directory)
    - [Processes Operations](#processes-operations)
      - [Get the status of a single process](#get-the-status-of-a-single-process)
      - [Get All Running Processes](#get-all-running-processes)
      - [Kill a Process](#kill-a-process)
    - [User Operations](#user-operations)
      - [Create a User](#create-a-user)
      - [Delete a User](#delete-a-user)
    - [System Information Retrieval](#system-information-retrieval)
      - [CPU Usage](#cpu-usage)
      - [Memory Usage](#memory-usage)
      - [Disk Usage](#disk-usage)
      - [Kernel Version](#kernel-version)
      - [OS Version](#os-version)
    - [Executing Commands with `run_cmd`](#executing-commands-with-run_cmd)

## Installation

You can install PySecureShellAutomator with pip:

```bash
pip install py_secure_shell_automator
```

## Usage

PySecureShellAutomator is designed to be easy to use. Here's an example of how to connect to a remote host and execute a command:

```python
from py_secure_shell_automator import PySecureShellAutomator

# Create a PySecureShellAutomator instance
ssh = PySecureShellAutomator(host='hostname', username='username', password='password')

# Use the PySecureShellAutomator instance to perform operations
processes = ssh.get_all_running_processes()

for process in processes:
    print(f"User: {process.user}, PID: {process.pid}, CPU: {process.cpu}, MEM: {process.mem}, Command: {process.command}")

    >>>User: root, PID: 1, CPU: 0.1, MEM: 1.4, Command: /sbin/init
    User: daemon, PID: 2, CPU: 0.0, MEM: 0.1, Command: /usr/sbin/atd -f
    User: root, PID: 3, CPU: 0.2, MEM: 0.8, Command: /usr/sbin/cron -f
    User: root, PID: 4, CPU: 0.5, MEM: 2.6, Command: /usr/sbin/rsyslogd -n
    User: syslog, PID: 5, CPU: 0.0, MEM: 0.3, Command: /usr/sbin/rsyslogd -n
    User: root, PID: 10, CPU: 0.3, MEM: 1.4, Command: /sbin/dhclient -1 -v -pf /run/dhclient.eth0.pid -lf /var/lib/dhcp/dhclient.eth0.leases eth0
    User: root, PID: 11, CPU: 0.0, MEM: 0.1, Command: /sbin/agetty --noclear tty1 linux
    User: root, PID: 12, CPU: 0.0, MEM: 0.1, Command: /sbin/agetty --keep-baud 115200 38400 9600 ttyS0 vt220
    User: root, PID: 13, CPU: 0.4, MEM: 2.2, Command: /usr/lib/postfix/sbin/master -w
    User: www-data, PID: 14, CPU: 2.0, MEM: 4.0, Command: /usr/sbin/apache2 -k start
```

## Establishing a Connection

PySecureShellAutomator allows you to establish an SSH connection to a remote Linux host using the paramiko library. You can customize the connection using several attributes:

- `host`: The hostname or IP address of the remote host.

- `username`: The username to use for the SSH connection.

- `password`: The password to use for the SSH connection. This is required for password-based authentication.

- `port`: The port to use for the SSH connection. The default is 22.

- `pkey`: The path to the private key file to use for the SSH connection. This is required for key-based authentication.

- `timeout`: The maximum amount of time (in seconds) to wait for the connection to be established. Default is 10 seconds.

- `auth_timeout`: The maximum amount of time (in seconds) to wait for authentication to complete. Default is 10 seconds.

- `auto_add_policy`: If set to True, the host's key will be automatically added to the known hosts file. This is useful if you're connecting to the host for the first time.

- `sftp`: If set to True, the SFTP protocol will be used for the connection. This is useful if you need to transfer files to/from the host.

Here's how you can establish a connection using password-based authentication and key-based authentication:

### Password-based Authentication

```python
pass_ssh = PySecureShellAutomator(host='hostname', username='username', password='password')
```

### Key-based Authentication

```python
key_ssh = PySecureShellAutomator(host='hostname', username='username', pkey='path_to_key')
```

Remember to replace 'hostname', 'username', 'password', and 'path_to_key' with your actual host details. Also, ensure that the user has the necessary permissions to establish the SSH connection.

### File Operations

PySecureShellAutomator provides methods for performing various file operations on the remote host.

Observation: TO use `sftp` operations, set `sftp=True` when creating the PySecureShellAutomator instance.

Methods that use `sftp`:

- copy_file_to_remote
- copy_file_from_remote

Here is an example of how to create a PySecureShellAutomator instance with `sftp` operations:

```python
# Create an instance of SSHFileOperations
ssh_file_ops = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
```

The other methods you are free to use without `sftp` set to `True`.
In the following examples, we will use the `ssh_file_ops` instance to perform file operations, for convenience, but again, you can use any instance of PySecureShellAutomator.

#### Copy a File to the Remote Host

```python
ssh_file_ops.copy_file_to_remote('local_path', 'remote_path')
```

#### Copy a File from the Remote Host

```python
ssh_file_ops.copy_file_from_remote('local_path', 'remote_path')
```

#### Get Content of a File

```python
ssh_file_ops.get_file_content('remote_path')
```

#### Create a Directory

```python
ssh_file_ops.create_directory('remote_path')
```

#### Get Scructure of a Directory

```python
structure = ssh_file_ops.get_directory_structure('path')
for directory in structure:
    print(f"Directory: {directory.dir}")
    print("Files:")
    for file in directory.files:
        print(file)
```

#### Remove a File

```python
ssh.remove_file('remote_file_path')
```

#### Remove Directory

```python
ssh.remove_directory('remote_path', recursive=False) # recursive=True to remove recursively, default is False
```

### Processes Operations

PySecureShellAutomator provides methods for performing various processes operations on the remote host. Here are some examples of how to use these methods:

#### Get the status of a single process

```python
processes = ssh.get_single_process_status('process_name')
for process in processes:
    print(f"User: {process.user}, PID: {process.pid}, CPU: {process.cpu}, MEM: {process.mem}, Command: {process.command}")
```

#### Get All Running Processes

```python
processes = ssh.get_all_running_processes()
for process in processes:
    print(f"User: {process.user}, PID: {process.pid}, CPU: {process.cpu}, MEM: {process.mem}, Command: {process.command}")
```

#### Kill a Process

```python
ssh.kill_process('process_name', run_as_root=False) # If necessary, set run_as_root=True to run as root, default is False
```

### User Operations

Manage user accounts on the remote host, including creating, modifying, and deleting users.

#### Create a User

```python
ssh.create_user('username', 'password', run_as_root=True) # By default, the command is executed as root. If necessary, set run_as_root=False to run as a non-root user.
```

#### Delete a User

```python
ssh.delete_user('username', run_as_root=True) # By default, the command is executed as root. If necessary, set run_as_root=False to run as a non-root user.
```

### System Information Retrieval

Retrieve comprehensive system information from the remote host, CPU usage, memory usage, and disk usage.

Observation: The following methods are not executed as root by default. If necessary, set run_as_root=True to run as root.

#### CPU Usage

```python
cpu_usage = ssh.get_cpu_usage()
print(f"CPU Usage: {cpu_usage}")
```

#### Memory Usage

```python
mem_usage = ssh.get_memory_usage()
print(f"Memory Usage: {mem_usage}")
```

#### Disk Usage

```python
disk_usage = ssh.get_disk_usage()
print(f"Disk Usage: {disk_usage}")
```

#### Kernel Version

```python
kernel_version = ssh.get_kernel_version()
print(f"Kernel version: {kernel_version}")
```

#### OS Version

```python
os_version = ssh.get_os_version()
print(f"OS: {ssh.os_version}")
```

### Executing Commands with `run_cmd`

The `run_cmd` method is a powerful tool in PySecureShellAutomator that allows you to execute any command on the remote host. This method provides a high level of flexibility and control, with several parameters to customize the command execution:

- `cmd`: This is the command you want to execute on the remote host. It can be any command that the remote system recognizes.

- `user`: This parameter allows you to specify the user that will execute the command. If not provided, the command will be executed with the same user that was used to establish the SSH connection.

- `raise_exception`: If set to True, the method will raise an exception if the command's exit code is not 0, i.e., if the command fails. This is useful if you want to ensure that the command was executed successfully.

- `custom_exception`: This parameter allows you to specify a custom exception that will be raised if the command fails and `raise_exception` is set to True. This can be useful for handling specific types of errors.

- `err_message`: This is the error message that will be used if an exception is raised. If not provided, the output of the command will be used as the error message.

- `cmd_timeout`: This parameter allows you to specify a timeout for the command execution. If the command does not complete within this time, it will be terminated. Default is 10 seconds.

The `run_cmd` method returns a `CmdResponse` object, which contains the output of the command and its exit code. You can use this object to check the result of the command and handle it in your code.

Here's an example of how to use the `run_cmd` method:

```python
from py_secure_shell_automator import PySecureShellAutomator

# Create a PySecureShellAutomator instance
ssh = PySecureShellAutomator(host='hostname', username='username', password='password')

# Create a custom command
command = 'uptime'

# Execute the custom command
output = ssh.run_cmd(command)

# Print the output
print(output.out)
# 16:38:59 up  1:02,  1 user,  load average: 0.00, 0.00, 0.00

# Print exit code
print(output.ext_code)
# 0

# Check if the command was successful
print(output.is_successful)
# True
```

