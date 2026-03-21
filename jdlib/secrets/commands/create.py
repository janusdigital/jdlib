import getpass
from argparse import ArgumentParser
from subprocess import CalledProcessError

from jdlib.cli import call_command
from jdlib.cli.commands import BaseCommand, ShellCommandMixin


class Command(BaseCommand, ShellCommandMixin):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('name')

    def handle(self, **options):
        name = options['name']
        result = call_command('secrets', 'get', name=name)
        if result is None:
            password = getpass.getpass('').strip()
            try:
                self.run_command([
                    'secret-tool', 'store',
                    '--collection=/org/freedesktop/secrets/collection/jdlib',
                    f'--label={name}',
                    'collection', 'jdlib', 'name', name,
                ], input=password)
            except CalledProcessError:
                pass
        else:
            self.stdout.write(f'{name} already exists.')
