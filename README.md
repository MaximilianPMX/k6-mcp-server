# k6-mcp-server

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project Overview

The `k6-mcp-server` is designed to receive and process data from the k6 load testing tool using the Model Context Protocol (MCP).  It provides a server that acts as a coordination point or data aggregation service, extendable via a plugin architecture. This enables seamless integration of k6 performance metrics with various monitoring and analysis tools.

**Key Features:**

*   **MCP Data Reception:**  Receives MCP formatted data from k6.
*   **Data Validation:**  Validates incoming MCP data to ensure data integrity.
*   **Plugin Architecture:** Allows for extending the server's functionality through plugins.
*   **Modular Design:**  Offers loose coupling and easy extensibility.
*   **Flask-based Core:** Built upon the Flask web framework for robustness and flexibility.
*   **Configuration Management:** Centralized configuration using `.ini` files.
*   **Logging:** Comprehensive logging for debugging and monitoring.

**Project Goals:**

*   Provide a robust and scalable MCP server for k6 load testing.
*   Enable easy integration with various monitoring and analysis tools through plugins.
*   Offer a flexible and extensible architecture for future enhancements.
*   Facilitate efficient data aggregation and coordination for complex load testing scenarios.

## Installation

### Prerequisites

*   Python 3.9 or higher
*   Poetry (dependency management)
*   Git (for cloning the repository)

### Installation Steps

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd k6-mcp-server
    ```

2.  **Install Poetry:**

    If you don't have Poetry installed, follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation). Commonly:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Make sure Poetry is added to your PATH. It may be required to restart your terminal or shell.

3.  **Install dependencies using Poetry:**

    ```bash
    poetry install
    ```

4.  **Activate virtual environment (optional, but recommended):**

    ```bash
    poetry shell
    ```

## Usage

### Basic Usage

1.  **Start the server:**

    ```bash
    poetry run gunicorn --bind 0.0.0.0:5000 wsgi:app
    ```
    This command uses Gunicorn to run the Flask application.  Ensure Gunicorn and other dependencies are installed (via `poetry install` as described above).  Access the server at `http://localhost:5000` (or the configured host and port).

2.  **Send MCP data from k6:**

    Configure k6 to send MCP data to the server's endpoint (e.g., `http://localhost:5000/mcp`).  Refer to the k6 documentation for details on configuring MCP output.

### Configuration

The server's configuration is managed via the `config/config.ini` file.  You can customize various settings, including:

*   **Server port:** The port the server listens on.
*   **Plugin directory:** The directory where plugins are located.
*   **Logging level:** The level of detail for logging.
*   **Any plugin-specific configurations**.

Edit the `config/config.ini` file to adjust these settings according to your needs:

```ini
[server]
port = 5000
debug = True

[logging]
level = INFO

[plugin_manager]
plugin_dir = src/plugins
```

### Examples

1.  **Sending data from k6:**

    ```javascript
    import http from 'k6/http';

    export default function () {
      const url = 'http://localhost:5000/mcp';
      const payload = JSON.stringify({
        "type": "metrics",
        "data": {
          "vus": 10,
          "iterations": 100
        }
      });
      const params = {
        headers: {
          'Content-Type': 'application/json',
        },
      };
      http.post(url, payload, params);
    }
    ```

2.  **Example Plugin (`src/plugins/examples/example_plugin.py`):**

    This example plugin demonstrates how to process received MCP data.

    ```python
    from k6_mcp_server.src.plugins.plugin_interface import PluginInterface

    class ExamplePlugin(PluginInterface): # must inherit from PluginInterface
        def __init__(self, config):
            super().__init__(config) # Call super constructor
            self.config = config #store config

        def process_data(self, data):
            """Process the received data."""
            print(f"Example Plugin received data: {data}") # Example action, print
            # Add your custom logic here
            return data
    ```

    To enable the plugin, ensure it is present in the `plugin_dir` (defined in `config.ini`) and the server will automatically load it.

## Project Structure

```
k6-mcp-server/
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements.txt
├── wsgi.py
├── config/
│   └── config.ini
├── logs/
├── src/
│   ├── app.py
│   ├── mcp/
│   │   ├── receiver.py
│   │   ├── validator.py
│   │   └── models.py
│   ├── plugins/
│   │   ├── plugin_manager.py
│   │   └── examples/
│   │       └── example_plugin.py
└── tests/
```

Key files and their purposes:

*   `wsgi.py`: Entry point for the Flask application to run with Gunicorn.
*   `src/app.py`: Main application file, initializes the Flask app, routes, and plugin manager.
*   `src/mcp/receiver.py`: Contains the logic for receiving MCP data.
*   `src/mcp/validator.py`: Defines the data validation logic.
*   `src/mcp/models.py`: Defines Pydantic models for MCP Data.
*   `src/plugins/plugin_manager.py`: Manages loading, registering, and executing plugins.
*   `src/plugins/examples/example_plugin.py`: An example plugin demonstrating the plugin architecture.
*   `requirements.txt`: Lists the project's dependencies, can be used in environments without poetry.
*   `pyproject.toml`: Defines dependencies and build system requirements for Poetry.
*   `config/config.ini`: Configuration file for the server and plugins.
*    `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `tests/`: Directory for Unit and Integration tests.

## Development

### Development Setup

1.  **Clone the repository:** (if you haven't already)

    ```bash
    git clone <repository_url>
    cd k6-mcp-server
    ```

2.  **Install dependencies using Poetry:** (if you haven't already)

    ```bash
    poetry install
    ```

3.  **Activate virtual environment (optional, but recommended):** (if you haven't already)

    ```bash
    poetry shell
    ```

4.  **Run tests:**

    ```bash
    poetry run pytest
    ```

    Ensure pytest is installed (`poetry add pytest --dev`).

### Contributing Guidelines

1.  **Fork the repository:** Create your own fork of the repository.
2.  **Create a branch:** Create a feature branch for your changes.
3.  **Implement your changes:** Make your changes, and add tests.
4.  **Run tests:** Ensure all tests pass.
5.  **Commit your changes:** Write clear and concise commit messages.
6.  **Push to your fork:** Push your branch to your forked respository.
7.  **Create a pull request:** Submit a pull request to the main repository.

    *   Follow the established code style.
    *   Include relevant tests.
    *   Address any feedback from reviewers.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   [k6](https://k6.io/) - For providing the load testing tool.
*   [Flask](https://flask.palletsprojects.com/) - For being the core web framework.
*   [Poetry](https://python-poetry.org/) - For Dependency management and packaging.
*   [Gunicorn](https://gunicorn.org/) - For providing a WSGI server.
*   [Pydantic](https://pydantic-docs.helpmanual.io/) - For enabling data validation, parsing, and management.
*   [pytest](https://docs.pytest.org/en/7.4.x/) - For Unit and Integrations tests.