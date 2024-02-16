import pytest
import os
from dotenv import load_dotenv

load_dotenv()

from py_secure_shell_automator import PySecureShellAutomator

PYSECURE_SHELL_AUTOMATOR_HOST = os.getenv("PYSECURE_SHELL_AUTOMATOR_HOST", "127.0.0.1")
PYSECURE_SHELL_AUTOMATOR_USERNAME = os.getenv(
    "PYSECURE_SHELL_AUTOMATOR_USERNAME", "root"
)
PYSECURE_SHELL_AUTOMATOR_PORT = int(os.getenv("PYSECURE_SHELL_AUTOMATOR_PORT", 22))
PYSECURE_SHELL_AUTOMATOR_PASSWORD = os.getenv(
    "PYSECURE_SHELL_AUTOMATOR_PASSWORD", "root"
)


@pytest.fixture
def ssh() -> PySecureShellAutomator:
    return PySecureShellAutomator(
        host=PYSECURE_SHELL_AUTOMATOR_HOST,
        username=PYSECURE_SHELL_AUTOMATOR_USERNAME,
        port=PYSECURE_SHELL_AUTOMATOR_PORT,
        password=PYSECURE_SHELL_AUTOMATOR_PASSWORD,
    )
