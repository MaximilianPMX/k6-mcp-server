import os
import sys
import logging
from flask import Flask, request, jsonify
import importlib
import yaml

# Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
plugins = []


def load_config(config_path='config.yaml'):
    """Loads configuration from a YAML file.
    Args:
        config_path (str): Path to the configuration file.
    Returns:
        dict: Configuration dictionary.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        return None


def load_plugins(plugin_paths):
    """Loads plugins from the specified paths.
    Args:
        plugin_paths (list): A list of paths to search for plugins.
    """
    for plugin_path in plugin_paths:
        # Ensure the path exists
        if not os.path.exists(plugin_path):
            logging.warning(f'Plugin path does not exist: {plugin_path}')
            continue

        # Add the plugin path to the system path so modules can be imported
        sys.path.append(plugin_path)

        for filename in os.listdir(plugin_path):
            if filename.endswith('_plugin.py'):
                module_name = filename[:-3]  # Remove '.py'
                try:
                    module = importlib.import_module(module_name)
                    # Check if the module has a 'plugin_class' attribute
                    if hasattr(module, 'plugin_class'):
                        plugin_class = getattr(module, 'plugin_class')
                        plugin_instance = plugin_class()
                        plugins.append(plugin_instance)
                        logging.info(f'Loaded plugin: {module_name}')
                    else:
                        logging.warning(f'Plugin {module_name} does not define a plugin_class.')
                except ImportError as e:
                    logging.error(f'Failed to import plugin {module_name}: {e}')
                except Exception as e:
                    logging.error(f'Error loading plugin {module_name}: {e}')
        # Remove the plugin path from the system path to avoid conflicts
        sys.path.remove(plugin_path)


@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    # Process data with each plugin
    for plugin in plugins:
        try:
            plugin.process_data(data)
        except Exception as e:
            logging.error(f'Error processing data with plugin {plugin.__class__.__name__}: {e}')

    return jsonify({'status': 'Data processed'}), 200


if __name__ == '__main__':
    config = load_config()
    if config:
        server_config = config.get('server', {})
        plugin_config = config.get('plugins', {})
        host = server_config.get('host', '0.0.0.0')
        port = server_config.get('port', 5000)
        plugin_paths = plugin_config.get('plugin_paths', [])

        load_plugins(plugin_paths)

        logging.info(f'Starting server on {host}:{port}')
        app.run(host=host, port=port, debug=True)
    else:
        logging.error('Failed to load configuration. Exiting.')
        sys.exit(1)
