import re

def extract_docstrings(content):
    # Regular expression for class definitions with docstrings
    class_pattern = re.compile(
        r'class\s+(\w+)\s*(\([\w, ]+\))?:\n\s+"""(.*?)"""',
        re.DOTALL
    )

    # Regular expression for method definitions with docstrings
    method_pattern = re.compile(
        r'def\s+(\w+)\s*\(.*?\)\s*->\s*.*?:\n\s+"""(.*?)"""',
        re.DOTALL
    )

    # Find all matches
    class_matches = class_pattern.findall(content)
    method_matches = method_pattern.findall(content)

    # Strip triple quotes from docstrings
    class_matches = [(cls[0], cls[1], cls[2].strip()) for cls in class_matches]
    method_matches = [(method[0], method[1].strip()) for method in method_matches]

    return class_matches, method_matches

def format_docstrings(class_matches, method_matches):
    formatted = []

    for cls in class_matches:
        class_name, base_classes, docstring = cls
        formatted.append(f"Class: {class_name}\nBase Classes: {base_classes}\nDocstring: {docstring}\n")

    for method in method_matches:
        method_name, docstring = method
        formatted.append(f"Method: {method_name}\nDocstring: {docstring}\n")

    return "\n".join(formatted)

# Test data
test_content = """
class SSHFileOperations(BaseSSH):
    \"\"\"
    Class to perform files operations on a remote machine
    \"\"\"

    def copy_file_to_remote(self, local_path: str, remote_path: str) -> None:
        \"\"\"
        Copies a file from the local machine to the remote host. `SFTP` must be initialized.
    
        The `local_path` and `remote_path` should be absolute paths, including the filename.
    
        If the file already exists at the `remote_path`, it will be overwritten.
    
        Args:
            local_path (str): Absolute path to the file on the local machine.
            remote_path (str): Absolute path where the file should be copied to on the remote host.
    
        Raises:
            SFTPNotInitializedError: If SFTP is not initialized.
            FileTransferError: If there is an error copying the file to the remote host.
    
        Examples:
            >>> py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
            >>> py_ssh.copy_file_to_remote('/absolute/path/to/local/file.txt', '/absolute/path/to/remote/file.txt')
        \"\"\"
        if not self._is_sftp_initialized:
            raise SFTPNotInitializedError("SFTP is not initialized")
        try:
            self._sftp.put(local_path, remote_path)
        except Exception as e:
            raise FileTransferError(f"Error copying file to remote: {e}")
    
    def copy_file_from_remote(self, remote_path: str, local_path: str) -> None:
        \"\"\"
        Copies a file from the remote host to the local machine. SFTP must be initialized.
    
        The `remote_path` and `local_path` should be absolute paths, including the filename.
    
        If the file already exists at the `local_path`, it will be overwritten.
    
        Args:
            remote_path (str): Absolute path to the file on the remote host.
            local_path (str): Absolute path where the file should be copied to on the local machine.
    
        Raises:
            SFTPNotInitializedError: If SFTP is not initialized.
            FileTransferError: If there is an error copying the file from the remote host.
    
        Examples:
            >>> py_ssh = PySecureShellAutomator(host='hostname', username='username', password='password', sftp=True)
            >>> py_ssh.copy_file_from_remote('/absolute/path/to/remote/file.txt', '/absolute/path/to/local/file.txt')
        \"\"\"
        if not self._is_sftp_initialized:
            raise SFTPNotInitializedError("SFTP is not initialized")
        try:
            self._sftp.get(remote_path, local_path)
        except Exception as e:
            raise FileTransferError(f"Error copying file from remote: {e}")
"""

# Extract docstrings
class_matches, method_matches = extract_docstrings(test_content)

# Format docstrings
formatted_docstrings = format_docstrings(class_matches, method_matches)

# Print formatted docstrings for verification
print(formatted_docstrings)