from plugin_interface import MCPPlugin

class ExamplePlugin(MCPPlugin):
    def process_data(self, data: dict):
        print(f"Example plugin received data: {data}")
        # Perform some action on the data
        # For example, extract some values and log them
        try:
            value = data['value']
            print(f"Extracted value: {value}")
        except KeyError:
            print("Value key not found in data.")