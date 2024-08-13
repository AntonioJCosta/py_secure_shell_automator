"""
Type Models of the package 
"""

from dataclasses import dataclass


@dataclass
class CmdResponse:
    """
    Command response of a remote command execution in a remote host.

    Attributes:
        ext_code (int): The exit code of the command.
        out (str): The output of the command.
    """

    ext_code: int
    out: str

    @property
    def is_successful(self) -> bool:
        """
        Return True if the command was executed successfully, False otherwise.

        Returns:
            bool: True if the exit code is 0, False otherwise.
        """
        return self.ext_code == 0


@dataclass
class Directory:
    """
    Content of a directory.

    Attributes:
        dir (str): The directory path.
        files (list[str]): List of files in the directory.
    """

    dir: str
    files: list[str]


@dataclass
class Process:
    """
    Content of a pprocess.

    Attributes:
        user (str): The user that started the process.
        pid (int): The process ID.
        cpu (float): The CPU usage of the process.
        mem (float): The memory usage of the process.
        command (str): The command that started the process.
    """

    user: str
    pid: int
    cpu: float
    mem: float
    command: str
