"""
Module to store the output of a command executed on linux and windows machines
"""

from dataclasses import dataclass


@dataclass
class CmdResponse:
    """
    Stores the output of a remote command execution on a linux or windows machine

    Attributes:
    ----------
    ext_code: exit code of the command
    out: output of the command
    """

    ext_code: int
    out: str

    @property
    def is_successful(self) -> bool:
        """
        Return True if the command was executed successfully, False otherwise
        """
        return self.ext_code == 0


@dataclass
class Directory:
    """
    Stores the content of a single directory

    Attributes:
    ----------
        dir: the directory path
        files: lislt of files in the directory
    """

    dir: str
    files: list[str]


@dataclass
class Process:
    """
    Stores the information of a process

    Attributes:
    ----------
        user: user that started the process
        pid: process id
        cpu: cpu usage of the process
        mem: memory usage of the process
        command: command that started the process
    """

    user: str
    pid: int
    cpu: float
    mem: float
    command: str
