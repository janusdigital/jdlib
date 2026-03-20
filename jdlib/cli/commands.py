import subprocess
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    help = ''

    def add_arguments(self, parser):
        pass

    @abstractmethod
    def handle(self, **options):
        pass


class ShellCommandMixin:
    """Mixin that provides shell command execution."""

    def run_command(self, command):
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
