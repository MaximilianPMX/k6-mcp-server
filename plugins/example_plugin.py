# plugins/example_plugin.py

def init_plugin(app):
    '''Initializes the plugin within the Flask app context'''
    print('Example plugin initialized!')

    # Example route added by the plugin
    @app.route('/plugin_route')
    def plugin_route():
        return 'This route is served by the example plugin!'
