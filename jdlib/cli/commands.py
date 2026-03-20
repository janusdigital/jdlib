from abc import ABC, abstractmethod


class BaseCommand(ABC):
    help = ''

    def add_arguments(self, parser):
        pass
    
    @abstractmethod
    def handle(self, **options):
        pass
