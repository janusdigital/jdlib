import getpass
import sys
from argparse import ArgumentParser
from subprocess import CalledProcessError

from jdlib.cli.commands import BaseCommand, ShellCommandMixin


class Command(BaseCommand, ShellCommandMixin):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('name')

    def handle(self, **options):
        name = options['name']
        password = getpass.getpass('').strip()
        try:
            self.run_command(f'echo "{password}" | secret-tool store --collection="/org/freedesktop/secrets/collection/jdlib" --label="{name}" collection jdlib name {name}')
        except CalledProcessError:
            sys.exit(1)
