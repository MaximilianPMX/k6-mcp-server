import asyncio
import importlib.util
import logging
import os


class PluginManager:
    """Manages the loading, processing, and unloading of plugins.

    Attributes:
        plugin_dir (str): The directory containing the plugin modules.
        logger (logging.Logger): The logger instance for logging messages.
        plugins (list): A list of loaded plugin instances.
    """

    def __init__(self, plugin_dir, logger):
        """Initializes the PluginManager.

        Args:
            plugin_dir (str): The directory containing the plugin modules.
            logger (logging.Logger): The logger instance for logging messages.
        """
        self.plugin_dir = plugin_dir
        self.logger = logger
        self.plugins = []

    async def load_plugins(self):
        """Loads all plugins from the plugin directory.

        Iterates through the files in the plugin directory,
        imports them as modules, and instantiates and loads the `Plugin` class
        if it exists.
        """
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = filename[:-3]
                file_path = os.path.join(self.plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, 'Plugin'):
                    try:
                        plugin_instance = module.Plugin(self.logger)
                        await plugin_instance.load()
                        self.plugins.append(plugin_instance)
                        self.logger.info(f'Plugin {module_name} loaded.')
                    except Exception as e:
                        self.logger.error(f'Failed to load plugin {module_name}: {e}')
                else:
                    self.logger.warning(f'Plugin {module_name} does not have a Plugin class.')

    def process_event(self, event_data):
        """Processes an event by passing it to each loaded plugin.

        Args:
            event_data (dict): The event data to process.
        """
        for plugin in self.plugins:
            try:
                asyncio.create_task(plugin.process(event_data))
            except Exception as e:
                self.logger.error(f'Error processing event with plugin {plugin.__class__.__name__}: {e}')

    async def unload_plugins(self):
        """Unloads all loaded plugins.

        Calls the `unload` method of each plugin and removes it from the
        list of loaded plugins.
        """
        for plugin in self.plugins:
            try:
                await plugin.unload()
                self.logger.info(f'Plugin {plugin.__class__.__name__} unloaded.')
            except Exception as e:
                self.logger.error(f'Error unloading plugin {plugin.__class__.__name__}: {e}')

            self.plugins.remove(plugin)