from flask import Flask, request, jsonify
import json

app = Flask(__name__)

REQUIRED_FIELDS = ['metric_name', 'value', 'timestamp']


def validate_mcp_data(data):
    """Validates the incoming MCP data.

    Args:
        data (dict): The MCP data to validate.

    Returns:
        tuple: A tuple containing a boolean indicating whether the data is valid,
               and an error message if the data is invalid (None otherwise).
    """
    if not isinstance(data, dict):
        return False, "Data must be a JSON object"

    for field in REQUIRED_FIELDS:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None


@app.route('/', methods=['POST'])
def receive_data():
    """Receives data from k6, validates it, and prints it.
    """
    try:
        data = request.get_json()

        is_valid, error_message = validate_mcp_data(data)

        if not is_valid:
            return jsonify({"error": error_message}), 400  # Bad Request

        print("Received valid data:", data)
        return jsonify({"message": "Data received successfully"}), 200  # OK

    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"error": str(e)}), 500  # Internal Server Error


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
