import subprocess
import sys
from abc import ABC, abstractmethod


class OutputWrapper:
    """A wrapper around a file-like object that appends a newline on write."""

    def __init__(self, out, ending='\n'):
        self._out = out
        self.ending = ending

    def write(self, msg='', ending=None):
        if msg is None:
            return
        if ending is None:
            ending = self.ending
        if msg and not msg.endswith(ending):
            msg += ending
        self._out.write(msg)


class BaseCommand(ABC):
    help = ''

    def __init__(self, stdout=None):
        self.stdout = OutputWrapper(stdout or sys.stdout)

    def add_arguments(self, parser):
        pass

    @abstractmethod
    def handle(self, **options):
        pass


class ShellCommandMixin:
    """Mixin that provides shell command execution."""

    def run_command(self, command, input=None):
        result = subprocess.run(command, check=True, capture_output=True, text=True, input=input)
        return result.stdout.strip()
