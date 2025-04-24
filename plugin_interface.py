from abc import ABC, abstractmethod

class MCPPlugin(ABC):
    @abstractmethod
    def process_data(self, data: dict):
        """Processes the MCP data.

        Args:
            data (dict): The MCP data to process.
        """
        pass