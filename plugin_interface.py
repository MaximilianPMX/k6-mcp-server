from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def process_data(self, data):
        pass