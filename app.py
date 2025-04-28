import asyncio
import logging
import signal

from aiohttp import web
import yaml

from plugin_interface import PluginManager


async def handle(request):
    """Handles incoming POST requests to the /data endpoint."""
    data = await request.json()
    request.app['plugin_manager'].process_event(data)
    return web.Response(text="Data received")


async def create_app(plugin_manager):
    """Creates the aiohttp web application.

    Args:
        plugin_manager: The PluginManager instance.

    Returns:
        An aiohttp web application instance.
    """
    app = web.Application()
    app['plugin_manager'] = plugin_manager
    app.router.add_post('/data', handle)
    return app


async def main():
    """Main function to set up and run the server.

    Loads configuration, initializes the plugin manager,
    creates the web application, and starts the server.
    """
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"Error: config.yaml not found: {e}")
        return
    except yaml.YAMLError as e:
        print(f"Error: invalid config.yaml: {e}")
        return

    logging.basicConfig(level=logging.getLevelName(config['log_level']))
    logger = logging.getLogger(__name__)

    plugin_manager = PluginManager(config['plugin_dir'], logger)
    await plugin_manager.load_plugins()

    app = await create_app(plugin_manager)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, config['host'], config['port'])
    await site.start()

    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, future.cancel)
    try:
        await future
    except asyncio.CancelledError:
        logger.info("Shutting down server...")
    finally:
        await runner.cleanup()
        await plugin_manager.unload_plugins()


if __name__ == '__main__':
    asyncio.run(main())