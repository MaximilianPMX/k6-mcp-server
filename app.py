from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    data = request.get_json()
    logger.info(f"Received MCP data: {data}")
    return 'Data received', 200

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
