import logging
from plugin_interface import PluginInterface

logger = logging.getLogger(__name__)

class FileLoggerPlugin(PluginInterface):
    def __init__(self, filename):
        self.filename = filename
        self.file_handler = logging.FileHandler(filename)
        self.file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        logger.addHandler(self.file_handler)
        logger.info(f"FileLoggerPlugin initialized, logging to {filename}")

    def process_data(self, data):
        try:
            logger.info(f"FileLoggerPlugin processing data: {data}")
        except Exception as e:
            logger.error(f"Error processing data in FileLoggerPlugin: {e}", exc_info=True)