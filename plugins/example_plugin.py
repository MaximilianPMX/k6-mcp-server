import asyncio
import logging


class Plugin:
    """Example plugin to demonstrate plugin structure."""

    def __init__(self, logger):
        """Initializes the plugin with a logger.

        Args:
            logger (logging.Logger): The logger instance for logging messages.
        """
        self.logger = logger
        self.name = 'Example Plugin'

    async def load(self):
        """Loads the plugin.  Placeholder for plugin initialization logic."""
        self.logger.info(f'{self.name} loading...')

    async def process(self, data):
        """Processes incoming data.

        Args:
            data (dict): The data to process.
        """
        self.logger.info(f'{self.name} processing data: {data}')
        await asyncio.sleep(1)
        self.logger.info(f'{self.name} finished processing data.')

    async def unload(self):
        """Unloads the plugin. Placeholder for plugin cleanup logic."""
        self.logger.info(f'{self.name} unloading...')