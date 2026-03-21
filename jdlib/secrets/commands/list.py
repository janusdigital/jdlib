from subprocess import CalledProcessError

from jdlib.cli.commands import BaseCommand, ShellCommandMixin


class Command(BaseCommand, ShellCommandMixin):
    def extract_labels(self, output: str):
        labels = []
        for line in output.split('\n'):
            if line.startswith('label ='):
                labels.append(line.split('=', 1)[1].strip())
        return labels

    def handle(self):
        try:
            output = self.run_command(['secret-tool', 'search', '--all', 'collection', 'jdlib'])
            for secret in sorted(self.extract_labels(output)):
                print(secret)
        except CalledProcessError:
            pass
