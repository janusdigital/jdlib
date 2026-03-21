import ast
import importlib
import importlib.util
import pkgutil
from argparse import ArgumentParser
from io import StringIO
from pathlib import Path

import jdlib


class JDCli:
    def __init__(self):
        self.parser = ArgumentParser(prog='jdcli')
        self.command_map = self.build_command_map()
        self.configure_parser()

    def run(self):
        """Parse arguments and run command."""
        args, remaining = self.parser.parse_known_args()

        if not args.module:
            self.parser.print_help()
            return

        if not args.command:
            self.module_parsers[args.module].print_help()
            return

        cmd = self.load_command(args.module, args.command)
        command_parser = ArgumentParser(
            prog=f'jdcli {args.module} {args.command}'
        )
        cmd.add_arguments(command_parser)
        command_args = command_parser.parse_args(remaining)
        cmd.handle(**vars(command_args))

    def build_command_map(self):
        """Build a mapping of module names to command names."""
        command_map = {}
        for module in self.get_command_modules():
            spec = importlib.util.find_spec(f'jdlib.{module}.commands')
            candidates = [
                name
                for _, name, is_pkg in pkgutil.iter_modules(
                    spec.submodule_search_locations
                )
                if not is_pkg and not name.startswith('_')
            ]
            command_map[module] = [
                name for name in candidates
                if self.has_command_class(module, name)
            ]
        return command_map

    def has_command_class(self, module, command):
        """Check if a command module has a `Command` class.`"""
        spec = importlib.util.find_spec(f'jdlib.{module}.commands.{command}')
        if spec is None or spec.origin is None:
            return False
        source = Path(spec.origin).read_text()
        tree = ast.parse(source)
        return any(
            isinstance(node, ast.ClassDef) and node.name == 'Command'
            for node in ast.iter_child_nodes(tree)
        )

    def configure_parser(self):
        """Register subparsers for each module and its commands."""
        module_subparsers = self.parser.add_subparsers(title='commands', dest='module')
        self.module_parsers = {}

        for module, commands in self.command_map.items():
            module_parser = module_subparsers.add_parser(module)
            self.module_parsers[module] = module_parser
            command_subparsers = module_parser.add_subparsers(title='commands', dest='command')

            for command_name in commands:
                command_subparsers.add_parser(command_name)

    def get_jdlib_modules(self):
        """Get all top level jdlib modules."""
        module_infos = pkgutil.iter_modules(jdlib.__path__)
        return [name for _, name, is_pkg in module_infos if is_pkg and name != 'cli']

    def get_command_modules(self):
        """Get all modules with a `commands` submodule."""
        modules = self.get_jdlib_modules()
        return [
            module
            for module in modules
            if importlib.util.find_spec(f'jdlib.{module}.commands') is not None
        ]

    def load_command(self, module, command):
        """Import a command module and return an instance of its `Command` class."""
        mod = importlib.import_module(f'jdlib.{module}.commands.{command}')
        return mod.Command()


def call_command(module, command, stdout=None, **kwargs):
    """Call a command programmatically."""
    if stdout is None:
        stdout = StringIO()
    mod = importlib.import_module(f'jdlib.{module}.commands.{command}')
    cmd = mod.Command(stdout=stdout)
    cmd.handle(**kwargs)
    if isinstance(stdout, StringIO):
        value = stdout.getvalue().strip()
        return value if value != '' else None


def main():
    JDCli().run()
