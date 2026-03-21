from argparse import ArgumentParser
from subprocess import CalledProcessError

from jdlib.cli.commands import BaseCommand, ShellCommandMixin


class Command(BaseCommand, ShellCommandMixin):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('name')

    def handle(self, **options):
        name = options['name']
        try:
            self.run_command(['secret-tool', 'clear', 'collection', 'jdlib', 'name', name])
        except CalledProcessError:
            pass
