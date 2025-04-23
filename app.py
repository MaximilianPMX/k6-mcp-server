from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mcp', methods=['POST'])
def handle_mcp_data():
    try:
        data = request.get_json()
        # Simulate processing the MCP data - replace with actual processing logic
        if not isinstance(data, dict):
            raise ValueError("Invalid MCP data format: Data must be a JSON object.")

        # Placeholder for actual data processing
        print("Received MCP data:", data)

        return jsonify({'message': 'MCP data received successfully'}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
