import json

class FileLoggerPlugin:
    def __init__(self):
        self.log_file = 'mcp_data.log'

    def process_data(self, data):
        try:
            with open(self.log_file, 'a') as f:
                json.dump(data, f)
                f.write('\n') # Add newline for readability
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def close(self):
        # Optional: close any resources if needed upon server shutdown
        pass