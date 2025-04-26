from flask import Flask, request, jsonify
import json
import importlib
import os
import plugin_interface  # Import the plugin_interface

app = Flask(__name__)

# Load plugins from the 'plugins' directory
plugins = []
plugin_directory = 'plugins'
for filename in os.listdir(plugin_directory):
    if filename.endswith('_plugin.py'):
        module_name = filename[:-3]
        try:
            module = importlib.import_module(f'{plugin_directory}.{module_name}')
            # Instantiate the plugin if it has a class named Plugin
            if hasattr(module, 'Plugin'):
                plugin_instance = module.Plugin()
                plugins.append(plugin_instance)
                print(f'Loaded plugin: {module_name}')
            else:
                print(f'Skipped loading {module_name}: No Plugin class found')
        except Exception as e:
            print(f'Error loading plugin {module_name}: {e}')


@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    data = request.get_json()
    print(f'Received data: {json.dumps(data)}')

    # Process data with each loaded plugin
    for plugin in plugins:
        try:
            plugin.process_data(data)
        except Exception as e:
            print(f'Error processing data with plugin {plugin.__class__.__name__}: {e}')

    return jsonify({'status': 'success', 'message': 'Data processed by plugins'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)