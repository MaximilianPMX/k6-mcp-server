import logging
from plugin_interface import PluginInterface

logger = logging.getLogger(__name__)

class ExamplePlugin(PluginInterface):
    def __init__(self):
        logger.info("ExamplePlugin initialized")

    def process_data(self, data):
        try:
            logger.info(f"ExamplePlugin processing data: {data}")
            # Simulate some processing of the data
            processed_data = f"Processed: {data['data']}"
            logger.debug(f"Data processed: {processed_data}")  # Log processed data

        except Exception as e:
            logger.error(f"Error processing data in ExamplePlugin: {e}", exc_info=True)