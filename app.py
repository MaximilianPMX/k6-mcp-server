import os
import importlib

from flask import Flask

app = Flask(__name__)

PLUGIN_DIR = 'plugins'


def load_plugins():
    '''Loads plugins from the plugins directory.'''
    plugin_count = 0
    for filename in os.listdir(PLUGIN_DIR):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f'{PLUGIN_DIR}.{module_name}')
                print(f'Loaded plugin: {module_name}')
                # Optionally, call an initialization function in the plugin
                if hasattr(module, 'init_plugin'):
                    module.init_plugin(app)
                plugin_count += 1
            except Exception as e:
                print(f'Error loading plugin {module_name}: {e}')
    print(f'Total plugins loaded: {plugin_count}')
    return plugin_count

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    # Create the plugins directory if it does not exist
    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)
    
    load_plugins()
    app.run(debug=True)
