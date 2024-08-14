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

- [Installation](#installation)
- [Key Features](#key-features)
- [Usage](#usage)

## Installation

You can install PySecureShellAutomator with pip:

```bash
pip install py_secure_shell_automator
```

## Key Features

- [PySecureShellAutomator: A Comprehensive SSH Management Library in Python](#pysecureshellautomator-a-comprehensive-ssh-management-library-in-python)
  - [Contents](#contents)
  - [Installation](#installation)
  - [Key Features](#key-features)
  - [Usage](#usage)
    - [Key-based Authentication](#key-based-authentication)
    - [Attributes](#attributes)
    - [Custom Commands](#custom-commands)
      - [**run\_cmd**](#run_cmd)
    - [Process Operations](#process-operations)
      - [**get\_single\_process\_status**](#get_single_process_status)
      - [**kill\_process**](#kill_process)
      - [**get\_all\_running\_processes**](#get_all_running_processes)
    - [File Operations](#file-operations)
      - [**copy\_file\_to\_remote**](#copy_file_to_remote)
      - [**copy\_file\_from\_remote**](#copy_file_from_remote)
      - [**get\_file\_content**](#get_file_content)
      - [**remove\_file**](#remove_file)
      - [**remove\_directory**](#remove_directory)
      - [**create\_directory**](#create_directory)
      - [**get\_directory\_structure**](#get_directory_structure)
        - [**change\_owner**](#change_owner)
    - [User Operations](#user-operations)
      - [**create\_user**](#create_user)
      - [**delete\_user**](#delete_user)
    - [System Information](#system-information)
      - [**get\_cpu\_usage**](#get_cpu_usage)
      - [**get\_memory\_usage**](#get_memory_usage)
      - [**get\_disk\_usage**](#get_disk_usage)
      - [**get\_kernel\_version**](#get_kernel_version)
      - [**get\_os\_version**](#get_os_version)

## Usage

PySecureShellAutomator is designed to be easy to use. Here's an example of how to connect to a remote host and execute a command:

```python
from py_secure_shell_automator import PySecureShellAutomator

py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password')

cmd_response = py_ssh.run_cmd(cmd='whoami')
print(cmd_response.ext_code) # Output: 0
print(cmd_response.out) # Output: 'username'
print(cmd_response.is_successful) # Output: True
```

Execute a command as a different user

```python
cmd_response = py_ssh.run_cmd(user='another_user', cmd='whoami')
print(cmd_response.out) # Output: 'another_user'
```

Execute a command as root

```python
cmd_response = py_ssh.run_cmd(user='root', cmd='whoami')
print(cmd_response.out) # Output: 'root'
```

### Key-based Authentication

To connect to a remote host using key-based authentication, you can specify the path to the private key file when creating the PySecureShellAutomator object:

```python
py_ssh = PySecureShellAutomator(host='hostname', username='username', pkey='path_to_key')
```

### Attributes

- `host (str)`: Host to connect to the remote host.
- `username (str)`: Username to connect to the remote host.
- `password (str, optional)`: Password to connect to the remote host. Defaults to None.
- `port (int, optional)`: Port to connect to the remote host. Defaults to 22.
- `pkey (str, optional)`: Private key to connect to the remote host. Defaults to None.
- `timeout (int, optional)`: Timeout to connect to the remote host. Defaults to 10.
- `auth_timeout (int, optional)`: Authentication timeout to connect to the remote host. Defaults to 10.
- `auto_add_policy (bool, optional)`: Whether to add the host to the known hosts. Defaults to True.
- `sftp (bool, optional)`: Whether to use the SFTP protocol to connect to the remote host. Defaults to False.

Remember to replace 'hostname', 'username', 'password', and 'path_to_key' with your actual host details. Also, ensure that the user has the necessary permissions to establish the SSH connection.

### Custom Commands

You can run any command on the remote host using the `run_cmd` method. The method returns a `CommandResponse` object that contains the output, exit code, and success status of the command.

#### **run_cmd**

Execute a command on the remote host. If the exit code is not 0, raise an exception.

- **Args**

  `cmd (str):` Command to execute on the remote host.
  `user (str, optional):` User to execute the command. If None, the user is the same as the one used to connect. Defaults to None.
  `raise_exception (bool, optional):` If True, raise an exception if the exit code is not 0. Defaults to True.
  `custom_exception (Type[Exception], optional):` Custom exception to raise if the exit code is not 0 and raise_exception is True. Defaults to CmdError.
  `err_message (str, optional):` Error message to raise if the exit code is not 0 and raise_exception is True. If None, the output of the command is used. Defaults to None.
  `cmd_timeout (float, optional):` Timeout to execute the command. Defaults to 10 seconds.

- **Returns**

  `CmdResponse`: Object with the output and exit code of the command.

- **Raises**

  `custom_exception`: Raised if the exit code is not 0 and raise_exception is True. If not specified, a `CmdError` exception is raised.

- **Examples**

1. **Using try-except block**

   Basic usage of the `run_cmd` method with error handling, using a try-except block to deal with exceptions.

   ```python
   from py_secure_shell_automator.exceptions import CmdError

   try:
       cmd_response = py_ssh.run_cmd(cmd='wrong_command')
   except CmdError as e:
       print(e)  # Output: 'bash: wrong_command: command not found'
   # Continue with the error handling
   ```

2. **Using `raise_exception=False`**

   Use the `raise_exception=False`parameter to prevent the method from raising an exception when the exit code is not 0. You can then check the`is_success`attribute of the`CmdResponse` object to determine if the command was successful.

   ```python
   cmd_response = py_ssh.run_cmd(cmd='wrong_command', raise_exception=False)
   if not cmd_response.is_succ ess:
           print(cmd_response.out)  # Output: 'bash: wrong_command: command not found'
           # Continue with the error handling
   ```

3. **Dealing with different exit codes**

   You can check the exit code of the command response to determine the outcome of the command execution,
   handling different exit codes accordingly, for a more granular error handling approach.

   ```python
   cmd_response = py_ssh.run_cmd(cmd='sh /path/to/script.sh', raise_exception=False)
   match cmd_response.ext_code:
       case 0:
           print("The script was executed successfully")
       case 126:
           print("The script was not executable")
       case 127:
           print("The script was not found")
       case _:
           print(f"An unknown error occurred with exit code {cmd_response.exit_code}")
   ```

4. **Defining a custom exception:**

   Create a custom exception class that inherits from `Exception` to handle specific types of errors.

   ```python

   class CustomError(Exception):
       pass
   try:
       cmd_response = py_ssh.run_cmd(cmd='wrong_command', custom_exception=CustomError)
   except Exception as e: # Print the custom error type
       print(type(e)) # Output: <class '**main**.CustomError'>
   ```

5. **Using a custom error message**

   Use the `err_message` parameter to specify a custom error message to raise when the exit code is not 0, and the `raise_exception` parameter is set to True.
   This is useful when you want to provide a more descriptive error message to the user, and the command output alone is not sufficient or does not have an error message.

   ```python
   try:
       cmd_response = py_ssh.run_cmd(cmd='command_with_no_output', err_message='The command failed')
   except CmdError as e:
       print(e) # Output: 'The command failed'
   ```

### Process Operations

Perform operations related to processes on the remote host, such as getting the status of a process, killing a process, and listing all running processes.

#### **get_single_process_status**

Get the status of all processes with a given name on the remote host.

- **Args**

  `process (str)`: Name of the process to check.
  `run_as_root (bool, optional)`: Whether to run the command as root. Default is False.

- **Returns**

  `list[Process]`: A list of Process objects representing the running processes, containing the user, pid, cpu, mem, and command.

- **Raises**

  `GetProcessStatusError`: If there is an error while getting the process status.

- **Examples**

  ```python
  processes = py_ssh.get_single_process_status('nginx')
  for process in processes:
      print(process)
  ```

#### **kill_process**

Kill a process on the remote host.

- **Args**

  `process (str)`: Name of the process to kill.
  `run_as_root (bool, optional)`: Whether to run the command as root. Default is False.

- **Raises**

  `KillProcessError`: If there is an error while killing the process.

- **Examples**

  ```python
  py_ssh.kill_process('nginx')
  ```

#### **get_all_running_processes**

Get all running processes on the remote host.

- **Args**

  `run_as_root (bool, optional)`: Whether to run the command as root. Default is False.

- **Returns**

  `list[Process]`: List of Process objects representing the running processes, containing the user, pid, cpu, mem, and command.

- **Raises**

  `GetProcessesStatusError`: If there is an error while getting the process status.

- **Examples**

  ```python
  processes = py_ssh.get_all_running_processes()
  for process in processes:
      print(process)
  ```

### File Operations

Perform files operations on the remote host, such as copying files, reading file content, removing files, and creating directories.

#### **copy_file_to_remote**

Copies a file from the local machine to the remote host. `SFTP` must be initialized.
The `local_path` and `remote_path` should be absolute paths, including the filename.
If the file already exists at the `remote_path`, it will be overwritten.

- **Args**

  `local_path (str)`: Absolute path to the file on the local machine.
  `remote_path (str)`: Absolute path where the file should be copied to on the remote host.

- **Raises**

  `SFTPNotInitializedError`: If SFTP is not initialized.
  `FileTransferError`: If there is an error copying the file to the remote host.

- **Examples**

  ```python
  py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
  py_ssh.copy_file_to_remote('/absolute/path/to/local/file.txt', '/absolute/path/to/remote/file.txt')
  ```

#### **copy_file_from_remote**

Copies a file from the remote host to the local machine. SFTP must be initialized.
The `remote_path` and `local_path` should be absolute paths, including the filename.
If the file already exists at the `local_path`, it will be overwritten.

- **Args**

  `remote_path (str)`: Absolute path to the file on the remote host.
  `local_path (str)`: Absolute path where the file should be copied to on the local machine.

- **Raises**

  `SFTPNotInitializedError`: If SFTP is not initialized.
  `FileTransferError`: If there is an error copying the file from the remote host.

- **Examples**

  ```python
  py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
  py_ssh.copy_file_from_remote('/absolute/path/to/remote/file.txt', '/absolute/path/to/local/file.txt')
  ```

#### **get_file_content**

Gets the content of a file as a string.

- **Args**

  `filepath (str)`: Path to the file to read.
  `run_as_root (bool, optional)`: Whether to run the command as root. Defaults to False.

- **Returns**

  `str`: Content of the file as a string.

- **Raises**

  `GetFileContentError`: If there is an error getting the file content.

- **Examples**

  ```python
  content = py_ssh.get_file_content('/path/to/file.txt')
  print(content) # Output: 'File content'
  ```

#### **remove_file**

Remove a file in the remote host.

- **Args**

  `filepath (str)`: Path to the file to remove.
  `force (bool, optional)`: If True, remove the file even if it's write-protected. Defaults to False.
  `run_as_root (bool, optional)`: Whether to run the command as root. Defaults to False.

- **Raises**

  `FileRemovalError`: If there is an error removing the file.

- **Examples**

1. **Remove a file normally**

   ```python
   py_ssh.remove_file('/path/to/file.txt')
   ```

2. **Force remove a write-protected file**

   ```python
   py_ssh.remove_file('/path/to/protected_file.txt', force=True)
   ```

#### **remove_directory**

Remove a directory.

- **Args**

  `dirpath (str)`: The path to the directory to remove.
  `force (bool, optional)`: If True, remove the directory even if it's not empty. Defaults to False.
  `run_as_root (bool, optional)`: Whether to run the command as root. Defaults to False.

- **Raises**

  `DirectoryRemovalError`: If there is an error removing the directory.

- **Examples**

1. **Remove an empty directory**

   ```python
   py_ssh.remove_directory('/path/to/empty_directory')
   ```

2. **Force remove a non-empty directory**

   ```python
   py_ssh.remove_directory('/path/to/non_empty_directory', force=True)
   ```

3. **Remove a directory as root**

   ```python
   py_ssh.remove_directory('/path/to/directory', run_as_root=True)
   ```

4. **Force remove a non-empty directory as root**

   ```python
   py_ssh.remove_directory('/path/to/non_empty_directory', force=True, run_as_root=True)
   ```

#### **create_directory**

Create a directory. If the directory already exists, the command will not fail.

- **Args**

  `dirpath (str)`: The path to the directory to create.
  `run_as_root (bool, optional)`: Whether to run the command as root. Defaults to False.

- **Raises**

  `DirectoryCreationError`: If there is an error creating the directory.

- **Examples**

1. **Create a directory normally**

   ```python
   py_ssh.create_directory('/path/to/new_directory')
   ```

2. **Create a directory as root**

   ```python
    py_ssh.create_directory('/path/to/new_directory', run_as_root=True)
   ```

#### **get_directory_structure**

List the content of a directory on the remote server.
Ensure that the user has the necessary permissions to list the directory content at the specified path.

- **Args**

  `path (str)`: The path to the directory to list. This should be an absolute path.
  `run_as_root (bool, optional)`: Whether to run the command with root user privileges. Defaults to False.

- **Returns**

  `list[Directory]`: A list of Directory objects representing each directory and its files.

- **Raises**

  `ListDirectoryContentError`: If the command fails to list the directory content.

- **Examples**

  ```python
  dir_structure = py_ssh.get_directory_structure('/path/to/directory')
  for directory in dir_structure:
      print(f"Directory: {directory.dir}")
      print("Files:")
      for file in directory.files:
          print(f"{file}")
  ```

##### **change_owner**

Change the owner of a file or directory.

- **Args**

  `path (str)`: The path to the file or directory.
  `owner (str)`: The new owner.
  `recursive (bool, optional)`: If True, change the owner recursively. Defaults to False.
  `run_as_root (bool, optional)`: Whether to run the command as root. Defaults to False.

- **Raises**

  `OwnerChangeError`: If there is an error changing the owner.

- **Examples**

1. **Change the owner of a file:**

```python
py_ssh.change_owner('/path/to/file', 'new_owner')
```

2. **Change the owner of a directory:**

```python
  py_ssh.change_owner('/path/to/directory', 'new_owner')
```

3. **Change the owner of a directory and its contents recursively:**

```python
  py_ssh.change_owner('/path/to/directory', 'new_owner', recursive=True)
```

### User Operations

Perform operations related to users on the remote host, such as creating and deleting users.

#### **create_user**

Create a new user on the remote host.

- **Args**

  `username (str)`: The username of the new user.
  `password (str)`: The password of the new user.
  `run_as_root (bool)`: Whether to run the command as root. Default is True.

- **Raises**

  `UserCreationError`: If there is an error creating the user.

- **Examples**

  ```python
  py_ssh.create_user(username='newuser', password='newpassword')
  ```

#### **delete_user**

Delete a user on the remote host.

- **Args**

  `username (str)`: The username of the user to delete.
  `run_as_root (bool)`: Whether to run the command as root. Default is True.

- **Raises**

  `UserDeletionError`: If there is an error deleting the user.

- **Examples**

  ```python
  py_ssh.delete_user(username='olduser')
  ```

### System Information

Collect system information from the remote host, such as CPU usage, memory usage, disk usage, kernel version, and operating system version.

#### **get_cpu_usage**

Get the CPU usage of the remote host.

- **Args**

  `run_as_root (bool)`: Whether to run the command as root. Default is False.

- **Returns**

  `str`: CPU usage.

- **Raises**

  `GetSystemInfoError`: If there is an error retrieving the CPU usage.

- **Examples**

  ```python
  print(cpu_usage) # Output: '10.0%'
  ```

#### **get_memory_usage**

Get the memory usage of the remote host.

- **Args**

  `run_as_root (bool)`: Whether to run the command as root. Default is False.

- **Returns**

  `str`: Memory usage.

- **Raises**

  `GetSystemInfoError`: If there is an error retrieving the memory usage.

- **Examples**

  ```python
  memory_usage = py_ssh.get_memory_usage()
  print(memory_usage) # Output: '10/20MB (50%)'
  ```

#### **get_disk_usage**

Get the disk usage of the remote host.

- **Args**

  `run_as_root (bool)`: Whether to run the command as root. Default is False.

- **Returns**

  `str`: Disk usage.

- **Raises**

  `GetSystemInfoError`: If there is an error retrieving the disk usage.

- **Examples**

  ```python
  disk_usage = py_ssh.get_disk_usage()
  print(disk_usage) # Output: '10/20GB (50%)'
  ```

#### **get_kernel_version**

Get the kernel version of the remote host.

- **Args**

  `run_as_root (bool)`: Whether to run the command as root. Default is False.
  `str`: Kernel version.

- **Raises**

  `GetSystemInfoError`: If there is an error retrieving the kernel version.

- **Examples**

  ```python
  kernel_version = py_ssh.get_kernel_version()
  print(kernel_version)
  '5.4.0-42-generic'
  ```

#### **get_os_version**

Get the operating system version of the remote host.

- **Args**

  `run_as_root (bool)`: Whether to run the command as root. Default is False.

- **Returns**

  `str`: Operating system version.

- **Raises**

  `GetSystemInfoError`: If there is an error retrieving the operating system version.

- **Examples**

  ```python
  os_version = py_ssh.get_os_version()
  print(os_version) # Output: 'Arch Linux'
  ```
