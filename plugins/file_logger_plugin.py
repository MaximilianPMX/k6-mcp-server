import asyncio
import json
import logging


class Plugin:
    """Plugin for logging data to a file."""

    def __init__(self, logger):
        """Initializes the plugin with a logger.

        Args:
            logger (logging.Logger): The logger instance for logging messages.
        """
        self.logger = logger
        self.name = 'File Logger Plugin'
        self.file_path = 'k6_data.log'

    async def load(self):
        """Loads the plugin.  Placeholder for plugin initialization logic."""
        self.logger.info(f'{self.name} loading...')

    async def process(self, data):
        """Processes incoming data by writing it to a file.

        Args:
            data (dict): The data to process.
        """
        try:
            with open(self.file_path, 'a') as f:
                f.write(json.dumps(data) + '\n')
            self.logger.info(f'{self.name} logged data to {self.file_path}')
        except Exception as e:
            self.logger.error(f'Error writing to file: {e}')
        await asyncio.sleep(0.1)

    async def unload(self):
        """Unloads the plugin. Placeholder for plugin cleanup logic."""
        self.logger.info(f'{self.name} unloading...')